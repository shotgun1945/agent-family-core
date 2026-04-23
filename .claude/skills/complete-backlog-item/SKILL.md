---
name: complete-backlog-item
description: Marks a backlog item as complete. Moves it from backlog.md (진행) to backlog_done.md with a completion date; moves linked planning docs to complete/ when applicable.
---

# Complete Backlog Item

## Workflow

### 1. 완료할 항목 확인
- 항목 미지정 시: `docs/00_backlog/backlog.md`의 **진행** 섹션을 보여주고 선택 요청
- 항목 지정 시: 진행 섹션에서 해당 항목 확인

### 2. backlog.md 업데이트
- **진행** 섹션에서 해당 항목 제거

### 3. backlog_done.md 업데이트
- **완료** 섹션에 항목 추가
- `ID` 필드 유지
- 형식: 항목 내용 + `(YYYY-MM-DD)` 완료일 추가

### 4. 기획 문서 이동 (해당 시)
- 항목의 **추가 문서** 필드에 경로가 있으면 `docs/10_planning/backlog/complete/`로 이동
- `git mv` 사용 (히스토리 보존)
- 대상 폴더 없으면 생성

### 5. 관련 문서 업데이트 (선택)
- 완료된 항목과 연관된 다른 문서가 있으면 업데이트 여부 확인

## 우선순위 정의
- `critical` — 즉시 처리, 다른 작업 블로킹
- `high` — 중요, 빠른 처리 필요
- `medium` — 일반 우선순위
- `low` — 여유 있을 때 처리

## 파일 경로
- 활성 백로그: `docs/00_backlog/backlog.md`
- 완료 아카이브: `docs/00_backlog/backlog_done.md`
- 기획문서(활성): `docs/10_planning/backlog/`
- 기획문서(완료): `docs/10_planning/backlog/complete/`
