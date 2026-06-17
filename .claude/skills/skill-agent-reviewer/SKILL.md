---
name: skill-agent-reviewer
description: "프로젝트의 스킬(.claude/skills/)·에이전트(.claude/agents/) 파일을 점검하고 개선하는 스킬. Grep-first 방식으로 전체 파일 Read 없이 메타 정보만 추출해 이슈를 진단한 뒤, 문제 파일만 부분 Read → Edit. '스킬 리뷰', '에이전트 점검', '스킬 개선', 'skill review', '스킬 파일 정리', '에이전트 파일 개선' 등의 표현에 트리거."
status: "v1.0"
---

## 이 스킬이 하는 일

`.claude/skills/` · `.claude/agents/` 파일들을 **최소 토큰**으로 점검하고 개선한다.

전체 파일을 읽지 않는다. Grep으로 메타 라인만 추출 → 이슈 가설 수립 → 해당 구간만 부분 Read → Edit.

---

## 진행 순서

### Step 1: 파일 목록 수집 (Glob 1회)

```
Glob(".claude/skills/**/*.md")
Glob(".claude/agents/*.md")
```

파일 경로 목록만 확인. 내용 Read 금지.

### Step 2: 메타 정보 일괄 Grep (Grep 1~2회)

아래 패턴을 **파일 전체에 한 번에** 실행해 메타 라인만 추출한다.

```
Grep(pattern="^name:|^description:|^model:|^tools:|^status:", path=".claude/")
```

추출 목표:
- `name` — 파일명과 일치하는지 확인
- `description` — 트리거 문구 포함 여부, 역할 설명 명확도
- `model` — 지정 여부
- `tools` — 필요 도구 누락 여부
- `status` — 버전 관리 여부

### Step 3: 이슈 패턴 Grep (선택적, 의심 파일만)

아래 안티패턴을 Grep으로 탐지한다.

| 안티패턴 | Grep 패턴 | 이슈 유형 |
|----------|----------|----------|
| 다른 파일 내용 중복 | `Grep("CLAUDE.md의 규칙과 동일한 핵심 문구")` | 중복 콘텐츠 |
| 잘못된 파일 참조 | `Grep("\.md\)")` → 경로 존재 여부 확인 | 깨진 링크 |
| Write 도구 없이 파일 생성 언급 | `Grep("Write\|파일 생성")` + tools 확인 | 도구 누락 |
| 역할 경계 불명확 | description에 "스킬"과 "에이전트" 동시 언급 | 역할 혼재 |

### Step 4: 이슈 목록 출력 → 사용자 확인

발견된 이슈를 아래 형식으로 출력하고, 처리 범위를 확인받는다.

```
## 점검 결과

### 발견된 이슈 (N건)
| # | 파일 | 이슈 유형 | 내용 |
|---|------|----------|------|
| 1 | vietnam-visit-report/SKILL.md | 중복 콘텐츠 | CLAUDE.md 편집 규칙 75줄 중복 |
| 2 | github-agent.md | 도구 누락 | Write 없이 Python 스크립트 생성 언급 |
| 3 | validator-agent.md | 범위 불명확 | AI 리포트 전용 루브릭인데 명시 없음 |

모두 수정할까요, 아니면 특정 이슈만 처리할까요?
```

### Step 5: 파일별 부분 Read → Edit

사용자 확인 후 이슈별로:

1. `Grep(이슈 관련 키워드, path=해당파일)` → 라인 번호 확인
2. `Read(offset=라인번호-5, limit=50)` — 해당 구간만
3. `Edit` — 최소 변경
4. 한 줄 완료 알림

**전체 파일 Read 절대 금지. 편집 내용 채팅 재출력 금지.**

---

## 점검 체크리스트 (이슈 유형 전체)

### 스킬 파일 (`SKILL.md`)

| # | 체크 항목 | 탐지 방법 |
|---|----------|----------|
| S1 | frontmatter `name`이 폴더명과 일치하는가 | Glob + name Grep 비교 |
| S2 | `description`에 트리거 문구가 명시됐는가 | description Grep → 키워드 확인 |
| S3 | `status` 버전이 기재됐는가 | status Grep |
| S4 | CLAUDE.md 규칙을 그대로 복사했는가 | 핵심 문구 Grep |
| S5 | 다른 스킬과 역할 중복이 있는가 | description 비교 |
| S6 | 참조 링크(`[파일](경로)`)가 유효한가 | 경로 Glob 확인 |
| S7 | 채팅 재출력 금지 · Grep-first 규칙을 내부에 명시했는가 | Grep("채팅 재출력\|Grep") |

### 에이전트 파일 (`.md`)

| # | 체크 항목 | 탐지 방법 |
|---|----------|----------|
| A1 | `model` 필드가 지정됐는가 | model Grep |
| A2 | `tools` 필드가 실제 역할에 맞게 선언됐는가 | tools Grep + 본문 기능 비교 |
| A3 | 스킬 SKILL.md가 있는데 내용을 중복 기재했는가 | 본문 길이 + SKILL.md 존재 여부 |
| A4 | description이 "언제 호출하는가"를 명확히 설명하는가 | description Grep |
| A5 | 스킬(직접 처리)과 에이전트(서브에이전트 스폰)의 역할이 구분됐는가 | description 비교 |

---

## 이슈 유형별 수정 패턴

| 이슈 유형 | 수정 방법 |
|----------|----------|
| 중복 콘텐츠 | 해당 블록 삭제 + `→ [CLAUDE.md](../../../CLAUDE.md) 참조` 한 줄로 대체 |
| 깨진 링크 | 올바른 경로로 교체 또는 링크 제거 |
| 도구 누락 | frontmatter `tools:` 에 추가 |
| 범위 불명확 | description 또는 본문 첫 줄에 적용 범위 명시 |
| 역할 경계 혼재 | description 재작성 — 스킬이면 "직접 처리", 에이전트면 "서브에이전트 스폰용" 명시 |
| 버전 누락 | frontmatter `status: "v1.0"` 추가 |

---

## 토큰 예산 목표

| 단계 | 허용 토큰 |
|------|----------|
| Step 1 Glob | ~500 |
| Step 2 메타 Grep | ~1,000 |
| Step 3 이슈 Grep (선택) | ~500 × 이슈 수 |
| Step 5 부분 Read | ~800 × 수정 파일 수 |
| **합계 (10파일 기준)** | **~8,000** |

전체 파일 Read 방식 대비 약 **70% 절약** 목표.

---

## 성공 기준

- [ ] 전체 파일 Read 없이 이슈 탐지 완료
- [ ] 사용자 확인 후 수정 실행
- [ ] 수정 파일별 한 줄 완료 알림
- [ ] SESSION_HANDOFF.md 스킬 현황 섹션 갱신
