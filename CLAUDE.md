---
updated: {SETUP_DATE}
version: 1
---

# {username}

## 프로젝트 목적
유저의 일상·업무·지식을 AI와 함께 관리하는 개인 AI 패밀리 시스템의 부모 프로젝트.

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

## 위키 (공유 지식)
- 단일 원천: `data/wiki/` — 쓰기(ingest·lint)는 이 저장소에서만, 자식은 읽기만 한다
- 검색·lint 도구: `scripts/wiki.py` (`search` / `lint`)
- 자식에 노출: `family-wiki` MCP 서버 (read-only) — `mcp_servers/wiki/` (등록 방법은 그 안 `README.md`, 키 merge 계약은 `data/children_manifest.md`의 `## MCP 서버 등록`)

## 스킬
- `lets-commit` → `.claude/skills/lets-commit/SKILL.md`
- `complete-backlog-item` → `.claude/skills/complete-backlog-item/SKILL.md`
- `create-child` → `.claude/skills/create-child/SKILL.md`
- `sync-to-children` → `.claude/skills/sync-to-children/SKILL.md`
- `sync-to-core` → `.claude/skills/sync-to-core/SKILL.md`

## 스킬·룰 추가 규칙 (구조 준수)

### 스킬 추가
- **원본(단일 진실 원천)**: `.claude/skills/<skill-name>/SKILL.md`
- **에이전트 호환 wrapper**: `.agents/skills/<skill-name>/SKILL.md`
- wrapper의 `name`/`description`은 원본과 **동일하게 유지**한다
- wrapper 본문은 **최소 내용**만 두고, 항상 원본 `.claude/skills/.../SKILL.md`를 읽고 따르도록 연결한다 (중복 작성 금지)

### 룰 추가
- 프로젝트의 거버넌스/작업 규칙은 항상 `CLAUDE.md`를 **단일 진실 원천**으로 유지한다
- Cursor 룰을 쓰는 경우:
  - `.cursor/rules/project-context.mdc`만 `alwaysApply: true`로 유지한다
  - 나머지는 `alwaysApply: false`로 별도 파일에 작성한다

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

- 기능·수정 작업이 끝나면 **커밋하기 전에** 해당 변경에 맞게 문서를 갱신한다.
- 갱신 대상은 변경 성격에 맞게 고른다: 사용자·실행 방법은 루트 `README` 등, 동작·구조·경계는 `docs/20_spec/` 등, 기획·백로그 연계는 `docs/10_planning/`·백로그 **추가 문서** 필드와 일치시킨다.
- **`src/`** 를 바꾼 경우에는 루트 `src/README.md`와, 영향이 있는 하위 폴더의 **`README.md`**(파일별 요약)도 커밋 전에 함께 맞춘다.
- **`docs/`** 를 바꾼 경우에는 루트 `docs/README.md`와, 영향이 있는 번호 폴더의 **`README.md`**(동일 폴더 문서 개략)도 커밋 전에 함께 맞춘다. **`docs/90_logs/`** 는 로그 파일을 나열하지 않고 **폴더·하위 구조 설명만** `README.md`에 유지한다.
- 순서 권장: 구현·테스트 확인 → 문서 반영 → 커밋(`.claude/skills/lets-commit/SKILL.md` 형식·분리 정책 준수).
- 문서화할 내용이 없다고 판단되면, 커밋 전에 그 사유를 짧게 정리해 두거나(커밋 본문·PR 설명) 대화에서 한 줄로 남긴다.
