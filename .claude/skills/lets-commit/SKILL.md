---
name: lets-commit
description: Applies reusable commit conventions. Use when preparing commits, grouping changes, or drafting commit messages.
---

# Let's Commit

## Message Format
- `<타입>: <한 줄 요약>`
- 예: `feat: add persona auto-update rule`
- 요약은 변경의 이유에 집중한다.

## Types
- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 동작 변경 없는 내부 재구성
- `docs`: 문서 변경
- `chore`: 유지보수·도구·설정
- `test`: 테스트 추가/수정
- `perf`: 성능 개선

## Commit Policy
1. 작업 단위로 분리한다.
2. 하나의 커밋 = 하나의 이유.
3. 관련 없는 변경을 섞지 않는다.

## Grouping Heuristic
- 같은 이유로 바뀐 파일 → 하나의 커밋
- 이유가 다르면 (예: docs + feature) → 분리
- 한 변경이 다른 변경을 활성화하면 → 함께 묶음

## Pre-Commit Checklist
- [ ] 커밋 범위가 단일 목적인가
- [ ] 타입이 변경의 주요 이유와 일치하는가
- [ ] 요약 줄이 변경 이유를 설명하는가
- [ ] 관련 문서/테스트가 같이 업데이트됐는가
