---
updated: {SETUP_DATE}
---

<!-- region: child-specific -->
> 📝 **이 영역은 이 프로젝트 전용입니다**
> - `sync-to-core` 또는 `sync-to-children` 실행 시 이 영역은 건드리지 않습니다
> - 프로젝트 목적, 범위, 페르소나 경로 등 이 프로젝트에 특화된 내용을 여기에 작성합니다

# {child-name}

## 프로젝트 목적
- {PROJECT_PURPOSE}

## 범위
- 포함: -
- 제외: -

## 부모 연동
- **전파 목록(매니페스트)** — 자식으로 복사하지 않음. 항상 부모만 참조: `../../{username}/data/children_manifest.md`
- 로컬 복사된 스킬(매니페스트 `자식 로컬 복사 매핑`):
  - `lets-commit`
  - `update-docs-from-conversation`
  - `sync-to-core`
  - `complete-backlog-item`
  - `wiki-query`
  - `wiki-ingest`
- 부모 페르소나 참조:
  - `../../{username}/data/persona/`
  - `../../{username}/data/persona/update_rules.md`

### 부모 Wiki 사용

- 공통 지식 위키는 `../../{username}/data/wiki/`를 단일 원천으로 사용한다.
- 자식에서 투자·개념·공통 의사결정 질문을 받으면 로컬 복사된 `wiki-query` 스킬을 따른다.
- 검색 보조는 부모 공용 스크립트를 호출한다:
  `python3 ../../{username}/scripts/wiki.py search "<질문 키워드>" --root ../../{username} --limit 8`
- wiki lint는 다음 명령으로 실행한다:
  `python3 ../../{username}/scripts/wiki.py lint --root ../../{username}`
- 자식에서 나온 재사용 가능한 분석은 `../../{username}/data/wiki/analysis/` 또는 관련 concept/entity에 filed-back한다.

## 유저 페르소나
- `../../{username}/data/persona/profile.md`
- `../../{username}/data/persona/preferences.md`
- `../../{username}/data/persona/personality.md`

## AI 페르소나
- `../../{username}/data/persona/assistant_persona.md`

## 페르소나 업데이트
- 저장 기준: `../../{username}/data/persona/update_rules.md`
- 조건에 맞는 정보는 `../../{username}/data/persona/`에 직접 반영

<!-- /region: child-specific -->

<!-- region: family-core source=propagated -->
> ⚠️ **이 영역은 부모에서 동기화됩니다**
> - 진실 원천: `../../{username}/data/templates/child_CLAUDE.md`의 `family-core` region
> - 이 영역을 직접 수정하면 다음 `sync-to-children` 실행 시 **덮어쓰여집니다**
> - 커스텀이 필요하다면:
>   1. 이 마커에 아래 속성을 추가하고 내용을 수정하세요
>      `modified=true modified-date=YYYY-MM-DD modified-reason="이유"`
>   2. 부모에서 `sync-to-children` 실행 시 자동으로 pinned 처리됩니다

## 백로그
- 활성 백로그: `docs/00_backlog/backlog.md` — **진행** / **대기** 섹션
- 완료 아카이브: `docs/00_backlog/backlog_done.md`
- 백로그 기획문서 : `docs/10_planning/backlog/` 폴더에 생성
- 완료 처리: `/complete-backlog-item` 스킬 사용; 완료된 기획 문서는 `docs/10_planning/backlog/complete` 폴더로 이동
- 백로그는 이 프로젝트 내부에서만 관리한다.

### 항목 필드 정의
- `ID` — 프로젝트 내 고유 식별자. 형식: `접두어-###` (세 자리 숫자, 예: `FP2-001`). 접두어는 README 또는 이 파일에 한 줄로 정한다. {username} 본 저장소 백로그는 `{BACKLOG_PREFIX}-###`. 신규 항목은 기존 최대 번호 + 1로 부여한다.
- `태그` — 작업 유형 분류 (예: `#feature`, `#fix`, `#chore`, `#docs`, `#refactor`)
- `제목` — 항목을 한 줄로 요약한 이름
- `우선순위` — 처리 긴급도
- `설명` — 작업 내용 및 목적을 간략히 기술
- `추가 문서` — 관련 스펙·설계 문서 경로 (없으면 `-`)
- `등록일` — 항목을 백로그에 추가한 날짜 (YYYY-MM-DD)

### 우선순위 단계
- `critical` — 즉시 처리, 다른 작업을 블로킹
- `high` — 중요, 빠른 시일 내 처리
- `medium` — 일반 우선순위
- `low` — 여유 있을 때 처리

## 개발 완료 후·커밋 전 문서화

- 기능·수정 작업이 끝나면 **커밋하기 전에** 해당 변경에 맞게 문서를 갱신한다.
- 갱신 대상은 변경 성격에 맞게 고른다: 사용자·실행 방법은 루트 `README` 등, 동작·구조·경계는 `docs/20_spec/` 등, 기획·백로그 연계는 `docs/10_planning/`·백로그 **추가 문서** 필드와 일치시킨다.
- **`src/`** 를 바꾼 경우에는 루트 `src/README.md`와, 영향이 있는 하위 폴더의 **`README.md`**(파일별 요약)도 커밋 전에 함께 맞춘다.
- **`docs/`** 를 바꾼 경우에는 루트 `docs/README.md`와, 영향이 있는 번호 폴더의 **`README.md`**(동일 폴더 문서 개략)도 커밋 전에 함께 맞춘다. **`docs/90_logs/`** 는 로그 파일을 나열하지 않고 **폴더·하위 구조 설명만** `README.md`에 유지한다.
- 순서 권장: 구현·테스트 확인 → 문서 반영 → 커밋(`.claude/skills/lets-commit/SKILL.md` 형식·분리 정책 준수).
- 문서화할 내용이 없다고 판단되면, 커밋 전에 그 사유를 짧게 정리해 두거나(커밋 본문·PR 설명) 대화에서 한 줄로 남긴다.

## `src/` 코드 탐색

- `src/` 및 하위 디렉터리(`core/`, `config/`, `storage/`, `clients/`, `nodes/`, `report/`, `pipelines/`, `scripts/`, `utils/` 등)에는 **`README.md`** 가 있으면, 폴더 전체를 소스 단위로 훑기 전에 **우선 `src/README.md` → 해당 폴더의 `README.md`** 를 읽어 역할·파일 요약을 파악한다.
- `README.md` 갱신 시점·범위는 위 **개발 완료 후·커밋 전 문서화**의 `src/`·`README.md` 항목을 따른다.

## `docs/` 문서 탐색

- 번호 폴더(`00_backlog/`, `10_planning/`, …)마다 **`README.md`** 를 두며, **그 폴더에 있는 문서 파일**을 표로 개략 설명한다. 탐색 순서: **`docs/README.md` → 해당 폴더 `README.md` → 본문**.
- **`docs/90_logs/`** 만 예외로, 개별 로그 `.md` 는 README에 **적지 않고** 폴더 역할·하위 경로만 적는다.

<!-- /region: family-core -->
