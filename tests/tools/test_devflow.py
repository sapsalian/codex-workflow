from __future__ import annotations

import subprocess
from pathlib import Path

from tools import devflow


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / 'repo'
    repo.mkdir()
    _run(['git', 'init'], repo)
    _run(['git', 'config', 'user.email', 'test@example.com'], repo)
    _run(['git', 'config', 'user.name', 'Test User'], repo)
    (repo / '.claude' / 'plans').mkdir(parents=True)
    (repo / '.venv' / 'bin').mkdir(parents=True)
    pytest_stub = repo / '.venv' / 'bin' / 'python'
    pytest_stub.write_text('#!/bin/sh\nif [ "$1" = "-m" ] && [ "$2" = "pytest" ]; then\n  exit 0\nfi\nexit 0\n', encoding='utf-8')
    pytest_stub.chmod(0o755)
    (repo / '.gitignore').write_text('', encoding='utf-8')
    (repo / 'README.md').write_text('seed\n', encoding='utf-8')
    _run(['git', 'add', '-A'], repo)
    _run(['git', 'commit', '-m', 'chore: init'], repo)
    return repo


def test_slugify_and_template() -> None:
    assert devflow.slugify('사용자 인증 기능 추가') == 'task'
    assert devflow.slugify('Add Retry Endpoint') == 'add-retry-endpoint'
    rendered = devflow.render_template('테스트 요구사항')
    assert 'Status: in-progress' in rendered
    assert '[⏳ 대기]' in rendered


def test_new_creates_plan(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    result = devflow.main(['new', 'Add Retry Endpoint'])
    assert result == 0
    plans = sorted((repo / '.claude' / 'plans').glob('*.md'))
    assert len(plans) == 1
    assert plans[0].name.endswith('add-retry-endpoint.md')


def test_resume_prefers_in_progress(monkeypatch, tmp_path: Path, capsys) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n'
        '### Phase 1: A [✅ 완료]\n'
        '### Phase 2: B [🔄 진행 중]\n'
        '### Phase 3: C [⏳ 대기]\n',
        encoding='utf-8',
    )

    result = devflow.main(['resume'])
    assert result == 0
    out = capsys.readouterr().out
    assert 'resume-phase: 2' in out


def test_check_phase_validates_commit_message(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n### Phase 1: A [🔄 진행 중]\n',
        encoding='utf-8',
    )

    result = devflow.main(['check-phase', '--phase', '1', '--message', 'invalid message'])
    assert result == 1


def test_complete_phase_marks_without_commit(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n'
        '### Phase 1: A [🔄 진행 중]\n'
        '### Phase 2: B [⏳ 대기]\n',
        encoding='utf-8',
    )
    _run(['git', 'add', str(plan)], repo)
    _run(['git', 'commit', '-m', 'chore: add plan'], repo)

    (repo / '.gitignore').write_text('docs/DEVELOP_WORKFLOW.md\n', encoding='utf-8')
    (repo / 'file.txt').write_text('change\n', encoding='utf-8')
    _run(['git', 'add', 'file.txt'], repo)
    before = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()

    result = devflow.main(['complete-phase', '--phase', '1', '--message', 'feat(devflow): finish phase'])
    assert result == 0

    updated = plan.read_text(encoding='utf-8')
    assert '### Phase 1: A [✅ 완료]' in updated
    after = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    assert before == after


def test_complete_plan_requires_all_phases(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n'
        '### Phase 1: A [✅ 완료]\n'
        '### Phase 2: B [⏳ 대기]\n',
        encoding='utf-8',
    )
    _run(['git', 'add', str(plan)], repo)
    _run(['git', 'commit', '-m', 'chore: add plan'], repo)

    result = devflow.main(['complete-plan', '--message', 'chore: complete plan'])
    assert result == 1


def test_complete_plan_updates_meta_without_commit(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n'
        '### Phase 1: A [✅ 완료]\n'
        '### Phase 2: B [✅ 완료]\n',
        encoding='utf-8',
    )
    _run(['git', 'add', str(plan)], repo)
    _run(['git', 'commit', '-m', 'chore: add plan'], repo)
    (repo / 'artifact.txt').write_text('done\n', encoding='utf-8')
    _run(['git', 'add', 'artifact.txt'], repo)
    before = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()

    result = devflow.main(['complete-plan', '--message', 'chore: finalize plan'])
    assert result == 0

    updated = plan.read_text(encoding='utf-8')
    assert 'Status: complete' in updated
    assert 'Completed:' in updated
    after = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    assert before == after


def test_complete_phase_with_commit_flag_creates_commit(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n'
        '### Phase 1: A [🔄 진행 중]\n',
        encoding='utf-8',
    )
    _run(['git', 'add', str(plan)], repo)
    _run(['git', 'commit', '-m', 'chore: add plan'], repo)
    (repo / 'file.txt').write_text('change\n', encoding='utf-8')
    _run(['git', 'add', 'file.txt'], repo)
    before = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()

    result = devflow.main(
        ['complete-phase', '--phase', '1', '--message', 'feat(devflow): finish phase', '--commit']
    )
    assert result == 0

    after = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    assert before != after
    changed = subprocess.run(
        ['git', 'show', '--name-only', '--pretty=format:', 'HEAD'],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert '.claude/plans/2026-03-09-test.md' not in changed


def test_check_phase_fails_on_untracked(monkeypatch, tmp_path: Path) -> None:
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)
    plan = repo / '.claude' / 'plans' / '2026-03-09-test.md'
    plan.write_text(
        '# T\n<!-- Created: 2026-03-09 | Status: in-progress -->\n\n## Phases\n\n### Phase 1: A [🔄 진행 중]\n',
        encoding='utf-8',
    )
    _run(['git', 'add', str(plan)], repo)
    _run(['git', 'commit', '-m', 'chore: add plan'], repo)

    (repo / 'untracked.txt').write_text('x\n', encoding='utf-8')
    result = devflow.main(['check-phase', '--phase', '1', '--message', 'feat(devflow): check'])
    assert result == 1
