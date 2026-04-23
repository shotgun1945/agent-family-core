---
updated: {SETUP_DATE}
version: 1
---

# {username}

## 프로젝트 목적
{PROJECT_PURPOSE}

## 언어 설정
- 기본 언어: **{LANGUAGE}**
- 모든 응답, 문서 작성, 파일 내용은 위 언어를 기본으로 사용한다
- 유저가 다른 언어로 말하면 그 언어를 따른다

## 에이전트 정체성
- AI 이름: **{AI_NAME}**
- 역할: 유저의 일상·업무·지식을 함께 관리하는 개인 AI 어시스턴트
- 페르소나 상세: `data/persona/assistant_persona.md`

## 유저 페르소나
- `data/persona/profile.md`
- `data/persona/preferences.md`
- `data/persona/personality.md`

## 페르소나 업데이트
- 저장 기준: `data/persona/update_rules.md`
- 조건에 맞는 정보는 `data/persona/`에 직접 반영

## 자식 관리
- **전파 목록(매니페스트)** — 자식에 복사되지 않음. 항상 이 파일만 참조: `data/children_manifest.md`
- **자식 레지스트리** — 등록된 자식 프로젝트 목록: `data/children_registry.md`
- 자식 경로: `../{username}_children/`

## 스킬
- `lets-commit` → `.claude/skills/lets-commit/SKILL.md`
- `complete-backlog-item` → `.claude/skills/complete-backlog-item/SKILL.md`
- `create-child` → `.claude/skills/create-child/SKILL.md`
- `install-plugin` → `.claude/skills/install-plugin/SKILL.md`
- `promote-to-plugin` → `.claude/skills/promote-to-plugin/SKILL.md`
- `sync-to-children` → `.claude/skills/sync-to-children/SKILL.md`
- `sync-to-core` → `.claude/skills/sync-to-core/SKILL.md`

## 백로그
- 활성 백로그: `docs/00_backlog/backlog.md` — **진행** / **대기** 섹션
- 완료 아카이브: `docs/00_backlog/backlog_done.md`
- 백로그 기획문서: `docs/10_planning/backlog/`
- 완료 처리: `/complete-backlog-item` 스킬 사용
- 백로그 ID 접두어: **`{BACKLOG_PREFIX}`** — 형식 `{BACKLOG_PREFIX}-###`

### 항목 필드 정의
- `ID` — 형식: `{BACKLOG_PREFIX}-###` (세 자리 숫자). 신규 항목은 기존 최대 번호 + 1
- `태그` — 작업 유형 (`#feature`, `#fix`, `#chore`, `#docs`, `#refactor`)
- `제목` — 항목을 한 줄로 요약
- `우선순위` — `critical` / `high` / `medium` / `low`
- `설명` — 작업 내용 및 목적
- `추가 문서` — 관련 문서 경로 (없으면 `-`)
- `등록일` — YYYY-MM-DD

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
