---
updated: {SETUP_DATE}
---

# {child-name}

## 프로젝트 목적
{PROJECT_PURPOSE}

## 범위
- 포함: -
- 제외: -

## 플러그인 정보
- 이 프로젝트는 **배포용 플러그인**이다
- 공개 배포 대상: 일반 사용자
- 릴리즈 노트: `docs/90_logs/CHANGELOG.md`

## 부모 연동
- **전파 목록(매니페스트)** — 자식으로 복사하지 않음. 항상 부모만 참조: `../../{username}/data/children_manifest.md`
- 로컬 복사된 스킬(매니페스트 `자식 로컬 복사 매핑`):
  - `lets-commit` → `.claude/skills/lets-commit/SKILL.md`
  - `complete-backlog-item` → `.claude/skills/complete-backlog-item/SKILL.md`
- 부모 페르소나 참조:
  - `../../{username}/data/persona/`
  - `../../{username}/data/persona/update_rules.md`

## 유저 페르소나
- `../../{username}/data/persona/profile.md`
- `../../{username}/data/persona/preferences.md`
- `../../{username}/data/persona/personality.md`

## AI 페르소나
- `../../{username}/data/persona/assistant_persona.md`

## 페르소나 업데이트
- 저장 기준: `../../{username}/data/persona/update_rules.md`
- 조건에 맞는 정보는 `../../{username}/data/persona/`에 직접 반영

## 백로그
- 활성 백로그: `docs/00_backlog/backlog.md` — **진행** / **대기** 섹션
- 완료 아카이브: `docs/00_backlog/backlog_done.md`
- 백로그 기획문서: `docs/10_planning/backlog/`
- 완료 처리: `/complete-backlog-item` 스킬 사용
- 백로그 ID 접두어: **`{BACKLOG_PREFIX}`** — 형식 `{BACKLOG_PREFIX}-###`

### 항목 필드 정의
- `ID` — 형식: `{BACKLOG_PREFIX}-###`. 신규 항목은 기존 최대 번호 + 1
- `태그` — `#feature`, `#fix`, `#chore`, `#docs`, `#refactor`
- `제목` — 항목을 한 줄로 요약
- `우선순위` — `critical` / `high` / `medium` / `low`
- `설명` — 작업 내용 및 목적
- `추가 문서` — 관련 문서 경로 (없으면 `-`)
- `등록일` — YYYY-MM-DD

## 배포 관리
- 기능 완료 후 `docs/90_logs/CHANGELOG.md`에 릴리즈 노트를 추가한다
- 버전 형식: `v{MAJOR}.{MINOR}.{PATCH}` (SemVer)
- 배포 전 체크리스트:
  1. `README.md` 최신 상태 확인
  2. `CHANGELOG.md` 항목 추가
  3. `/lets-commit` 스킬로 커밋

## 개발 완료 후·커밋 전 문서화
- 기능·수정 작업이 끝나면 커밋 전에 관련 문서를 갱신한다
- 커밋 규칙: `.claude/skills/lets-commit/SKILL.md` 준수

## 배치 문서 업데이트
- 트리거 충족 시 문서 1개 이상 업데이트 또는 미업데이트 사유 보고
- 응답 끝에 아래 블록 포함:

```text
[배치 문서 업데이트]
- trigger: <value>
- updated_files:
  - <path or 없음>
- notes:
  - <1-3 lines>
```
