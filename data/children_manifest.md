---
updated: {SETUP_DATE}
---

# 자식 프로젝트 전파 매니페스트

자식 프로젝트 **생성**(`create-child`) 또는 **룰 전파**(`sync-to-children`) 시, **어떤 스킬·문서를 연결할지** 여기서만 정의한다.  
기본은 자식 `CLAUDE.md`에 **참조 경로**를 넣고, 필요 시 `sync-to-children`으로 **아래 `자식 로컬 복사 매핑`에 있는 항목만** 자식 로컬로 복사해 동기화한다.

## 배포 금지 — 이 매니페스트 파일 자체

**`data/children_manifest.md`는 자식 프로젝트로 복사·배포하지 않는다.**

- 단일 진실 원천은 **부모(Family Core)** 저장소의 이 파일뿐이다.
- 자식에서는 **`../../{username}/data/children_manifest.md`** 로만 읽는다.
- `sync-to-children`, `create-child`, `sync-to-core` 실행 시에도 이 파일은 복사 대상에 넣지 않는다.

---

## 자식 로컬 복사 매핑 (sync 기준)

`sync-to-children`은 **아래 표만** 읽어서 복사 대상을 결정한다.  
표에 없는 파일은 복사하지 않는다.

| ID | 종류 | 부모 소스 경로 | 자식 대상 경로 |
|----|------|----------------|----------------|
| `lets-commit-skill` | skill | `.claude/skills/lets-commit/SKILL.md` | `.claude/skills/lets-commit/SKILL.md` |
| `complete-backlog-item-skill` | skill | `.claude/skills/complete-backlog-item/SKILL.md` | `.claude/skills/complete-backlog-item/SKILL.md` |

---

## 자식 `CLAUDE.md`에 넣을 섹션

전파 후 자식 문서에 다음 섹션이 있어야 한다.

- `## 부모 연동` — 매니페스트는 부모만 참조: `../../{username}/data/children_manifest.md`

권장 문구:

```markdown
## 부모 연동
- **전파 목록(매니페스트)** — 자식으로 복사하지 않음. 항상 부모만 참조: `../../{username}/data/children_manifest.md`
- 로컬 복사된 스킬(매니페스트 `자식 로컬 복사 매핑`):
  - `lets-commit` → `.claude/skills/lets-commit/SKILL.md`
  - `complete-backlog-item` → `.claude/skills/complete-backlog-item/SKILL.md`
- 부모 페르소나 참조(상대 경로):
  - `../../{username}/data/persona/`
  - `../../{username}/data/persona/update_rules.md`
```

---

## 스킬 목록 (컨트롤)

| 스킬 name | 경로 | 언제 쓰는지 |
|-----------|------|-------------|
| `create-child` | `.claude/skills/create-child/SKILL.md` | 새 자식 프로젝트 생성 |
| `sync-to-children` | `.claude/skills/sync-to-children/SKILL.md` | 기존 자식에 스킬·문서 재동기화 |
| `sync-to-core` | `.claude/skills/sync-to-core/SKILL.md` | 자식 변경을 부모로 역전파 |

---

## 변경 절차

1. 이 파일(`data/children_manifest.md`) 수정
2. `sync-to-children`으로 각 자식 `CLAUDE.md`의 `## 부모 연동` 섹션 갱신
3. 필요 시 `data/children_registry.md`에 운영 메모 추가
4. 새 스킬 추가 시, 자식 복사 배포 대상 여부를 확인 후 `자식 로컬 복사 매핑` 표에 반영
