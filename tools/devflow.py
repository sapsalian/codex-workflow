from __future__ import annotations

import argparse
import datetime as dt
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PLAN_DIR = Path('.claude/plans')
META_RE = re.compile(r"<!--\s*Created:\s*([^|>]+)\|\s*Status:\s*([^|>]+)(?:\|\s*Completed:\s*([^>]+))?\s*-->")
PHASE_LINE_RE = re.compile(r"^(###\s+Phase\s+(?P<number>\d+):.*)\[(?P<status>⏳\s*대기|🔄\s*진행 중|✅\s*완료)\](?P<suffix>.*)$")
COMMIT_RE = re.compile(r"^(feat|fix|chore|refactor|test|docs)(\([a-z0-9._/-]+\))?: .+")


class DevflowError(RuntimeError):
    pass


@dataclass
class PhaseInfo:
    number: int
    status: str
    line: str


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=capture,
        text=True,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        detail = stderr or stdout or f'command failed: {cmd}'
        raise DevflowError(detail)
    return result


def today() -> str:
    return dt.date.today().isoformat()


def slugify(text: str) -> str:
    lowered = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or 'task'


def ensure_plan_dir() -> None:
    PLAN_DIR.mkdir(parents=True, exist_ok=True)


def render_template(requirement: str) -> str:
    created = today()
    return f"""# {requirement}\n<!-- Created: {created} | Status: in-progress -->\n\n## Context\n{requirement} 구현을 위한 /develop 워크플로우 실행 계획\n\n## Phases\n\n### Phase 1: 요구사항 정리 및 설계 [⏳ 대기]\n목표: 구현 범위와 검증 기준 확정\n- Step 1: Q&A 라운드 완료\n- Step 2: 테스트 전략 확정\n\n### Phase 2: 구현 및 검증 [⏳ 대기]\n목표: 기능 구현, 테스트 통과, 커밋 완료\n- Step 1: 테스트 작성 및 통과\n- Step 2: 구현 + 검증\n\n---\n"""


def list_plan_files() -> list[Path]:
    if not PLAN_DIR.exists():
        return []
    return sorted(PLAN_DIR.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)


def file_contains_in_progress(path: Path) -> bool:
    return 'Status: in-progress' in path.read_text(encoding='utf-8')


def resolve_plan(path_arg: str | None, require_in_progress: bool = True) -> Path:
    if path_arg:
        path = Path(path_arg)
        if not path.exists():
            raise DevflowError(f'plan file not found: {path}')
        return path

    plans = list_plan_files()
    if not plans:
        raise DevflowError('no plan files found under .claude/plans')

    if require_in_progress:
        in_progress = [p for p in plans if file_contains_in_progress(p)]
        if not in_progress:
            raise DevflowError('no in-progress plan file found')
        return in_progress[0]

    return plans[0]


def parse_phases(content: str) -> list[PhaseInfo]:
    phases: list[PhaseInfo] = []
    for line in content.splitlines():
        match = PHASE_LINE_RE.match(line)
        if not match:
            continue
        phases.append(
            PhaseInfo(
                number=int(match.group('number')),
                status=match.group('status'),
                line=line,
            )
        )
    return phases


def mark_phase(content: str, phase_number: int, status_text: str) -> str:
    target = f'[{status_text}]'
    lines = content.splitlines()
    replaced = False

    for idx, line in enumerate(lines):
        match = PHASE_LINE_RE.match(line)
        if not match:
            continue
        if int(match.group('number')) != phase_number:
            continue
        lines[idx] = f"{match.group(1)}{target}{match.group('suffix')}"
        replaced = True
        break

    if not replaced:
        raise DevflowError(f'phase not found: {phase_number}')

    return '\n'.join(lines) + ('\n' if content.endswith('\n') else '')


def update_plan_status(content: str, status: str) -> str:
    match = META_RE.search(content)
    if not match:
        raise DevflowError('plan meta header not found')

    created = match.group(1).strip()
    completed = match.group(3).strip() if match.group(3) else None
    if status == 'complete':
        completed = today()

    completed_part = f" | Completed: {completed}" if completed else ''
    new_meta = f"<!-- Created: {created} | Status: {status}{completed_part} -->"
    return content[: match.start()] + new_meta + content[match.end() :]


def validate_commit_message(message: str) -> None:
    if not COMMIT_RE.match(message):
        raise DevflowError(
            'invalid commit message. expected conventional style: '
            'feat(scope): ..., fix(scope): ..., chore: ..., refactor(scope): ..., test(scope): ..., docs(scope): ...'
        )


def check_git_state() -> None:
    run(['git', 'rev-parse', '--is-inside-work-tree'])
    status = run(['git', 'status', '--porcelain']).stdout.splitlines()

    unmerged_prefixes = {'DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'}
    for line in status:
        if line[:2] in unmerged_prefixes:
            raise DevflowError('git has unmerged/conflicted changes')
        if line.startswith('?? '):
            raise DevflowError('unexpected untracked files detected. stage or remove them before complete-* commands')


def run_tests(test_cmd: str) -> None:
    cmd = shlex.split(test_cmd)
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise DevflowError(f'test command failed: {test_cmd}')


def commit_all(message: str) -> None:
    # Keep workflow state local: never include .claude content in commits.
    run(['git', 'add', '-A', '--', '.', ':(exclude).claude/**'])
    result = run(['git', 'commit', '-m', message], check=False)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        detail = stderr or stdout or 'git commit failed'
        raise DevflowError(detail)


def command_new(args: argparse.Namespace) -> int:
    requirement = args.requirement.strip()
    if not requirement:
        raise DevflowError('requirement must not be empty')

    ensure_plan_dir()
    base_name = f"{today()}-{slugify(requirement)}"
    candidate = PLAN_DIR / f'{base_name}.md'
    suffix = 2
    while candidate.exists():
        candidate = PLAN_DIR / f'{base_name}-{suffix}.md'
        suffix += 1

    candidate.write_text(render_template(requirement), encoding='utf-8')
    print(candidate)
    return 0


def command_resume(args: argparse.Namespace) -> int:
    plan_path = resolve_plan(args.plan, require_in_progress=False)
    content = plan_path.read_text(encoding='utf-8')
    phases = parse_phases(content)
    in_progress = [p for p in phases if p.status.startswith('🔄')]
    waiting = [p for p in phases if p.status.startswith('⏳')]

    target = in_progress[0] if in_progress else (waiting[0] if waiting else None)
    print(f'plan: {plan_path}')
    if target:
        print(f'resume-phase: {target.number} ({target.status})')
    else:
        print('all phases complete')
    return 0


def command_check_phase(args: argparse.Namespace) -> int:
    validate_commit_message(args.message)
    check_git_state()
    run_tests(args.test_cmd)

    plan_path = resolve_plan(args.plan, require_in_progress=True)
    content = plan_path.read_text(encoding='utf-8')
    phases = parse_phases(content)
    if not any(p.number == args.phase for p in phases):
        raise DevflowError(f'phase not found in plan: {args.phase}')

    print('check-phase: PASS')
    return 0


def command_complete_phase(args: argparse.Namespace) -> int:
    validate_commit_message(args.message)
    check_git_state()
    run_tests(args.test_cmd)

    plan_path = resolve_plan(args.plan, require_in_progress=True)
    content = plan_path.read_text(encoding='utf-8')

    phases = parse_phases(content)
    target = next((p for p in phases if p.number == args.phase), None)
    if not target:
        raise DevflowError(f'phase not found in plan: {args.phase}')
    if target.status.startswith('✅'):
        raise DevflowError(f'phase already complete: {args.phase}')

    updated = mark_phase(content, args.phase, '✅ 완료')
    plan_path.write_text(updated, encoding='utf-8')
    if args.commit:
        commit_all(args.message)
        print(f'phase {args.phase} marked complete and committed')
    else:
        print(f'phase {args.phase} marked complete')
    return 0


def command_complete_plan(args: argparse.Namespace) -> int:
    validate_commit_message(args.message)
    check_git_state()
    run_tests(args.test_cmd)

    plan_path = resolve_plan(args.plan, require_in_progress=True)
    content = plan_path.read_text(encoding='utf-8')
    phases = parse_phases(content)
    if any(not p.status.startswith('✅') for p in phases):
        raise DevflowError('cannot complete plan: unfinished phases exist')

    updated = update_plan_status(content, 'complete')
    plan_path.write_text(updated, encoding='utf-8')
    if args.commit:
        commit_all(args.message)
        print('plan marked complete and committed')
    else:
        print('plan marked complete')
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='python -m tools.devflow')
    subparsers = parser.add_subparsers(dest='command', required=True)

    new_parser = subparsers.add_parser('new')
    new_parser.add_argument('requirement')
    new_parser.set_defaults(func=command_new)

    resume_parser = subparsers.add_parser('resume')
    resume_parser.add_argument('--plan', default=None)
    resume_parser.set_defaults(func=command_resume)

    check_parser = subparsers.add_parser('check-phase')
    check_parser.add_argument('--phase', type=int, required=True)
    check_parser.add_argument('--message', required=True)
    check_parser.add_argument('--test-cmd', default='.venv/bin/python -m pytest')
    check_parser.add_argument('--plan', default=None)
    check_parser.set_defaults(func=command_check_phase)

    phase_parser = subparsers.add_parser('complete-phase')
    phase_parser.add_argument('--phase', type=int, required=True)
    phase_parser.add_argument('--message', required=True)
    phase_parser.add_argument('--test-cmd', default='.venv/bin/python -m pytest')
    phase_parser.add_argument('--plan', default=None)
    phase_parser.add_argument('--commit', action='store_true')
    phase_parser.set_defaults(func=command_complete_phase)

    plan_parser = subparsers.add_parser('complete-plan')
    plan_parser.add_argument('--message', required=True)
    plan_parser.add_argument('--test-cmd', default='.venv/bin/python -m pytest')
    plan_parser.add_argument('--plan', default=None)
    plan_parser.add_argument('--commit', action='store_true')
    plan_parser.set_defaults(func=command_complete_plan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except DevflowError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
