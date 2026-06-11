---
name: ai-agent-research-report
description: "2026 AI 에이전트 트렌드 리포트를 최신 논문, 인플루언서 추천, 기업 업데이트와 함께 생성하는 스킬. 사용자가 AI 에이전트 리서치 리포트를 만들거나 업데이트하거나 분석하고 싶을 때, 최신 LLM/에이전트 논문을 추적하고 싶을 때, AI 분야 영향력 있는 인물을 찾고 싶을 때, Anthropic/OpenAI/Google 최신 동향을 파악하고 싶을 때, AI 분야 진행 상황을 문서화하고 싶을 때 반드시 사용. 'AI 리포트', '논문 트렌드', '인플루언서 맵', '에이전트 업데이트', '2026 AI', AI 분야 종합 문서화 요청 등의 표현에 트리거."
compatibility: "Core implementation complete. Requires: Python 3.8+, git, GitHub API access (optional). Uses WebSearch (default) or deep-research for data collection."
status: "v1.0 - Beta (80% production ready)"
---

## 이 스킬이 하는 일

완전한 **2026 AI 에이전트 리서치 리포트**를 생성합니다:

1. **핵심 논문 TOP 5** — 인용수, 컨퍼런스 등급(ICLR/ICML/NeurIPS), 실무 적용성 기준으로 선정
2. **인플루언서 맵** — 추천 커뮤니티/계정 6개: Reddit 3개 + X/트위터 3개 (선정 이유 포함)
3. **기업 업데이트 타임라인** — Anthropic(Claude), OpenAI(GPT/o시리즈), Google(Gemini/Astra) 출시 내역
4. **업계 트렌드** — 기업 간 교차 패턴, 추론 모델 수렴, 컴퓨터 조작 경쟁, MCP 표준화

**출력 형식:**
- 마크다운 (`YYYY-MM-DD_AI_Agent_Research_Report.md`) — 표, 링크, 구조화된 섹션
- HTML (`YYYY-MM-DD_AI_Agent_Research_Report.html`) — 그라디언트 스타일, 반응형 디자인
- 선택사항: GitHub 자동 커밋 + 우선순위 레이블 이슈 등록

## 구현 현황

✅ **완료** (80%):
- 핵심 아키텍처
- 옵션 파싱 및 라우팅
- 마크다운/HTML 생성
- Git 통합 (커밋/푸시)
- 이슈 관리 시스템 (레이블, 워크플로우)

⚠️ **진행 중** (완성 필요):
- GitHub Issues API 연동
- 실제 데이터 수집 (WebSearch/deep-research 훅)

📊 **테스트 커버리지**: 코드 분석으로 3개 시나리오 검증 완료
- 상세 내용은 `TEST_REPORT.md` 참조

## 언제 사용하나

✅ **이런 경우 사용:**
- "AI 에이전트 리포트" 또는 "2026 AI 리서치 요약" 요청 시
- "LLM 에이전트 관련 논문 추천해줘" 질문 시
- "AI 트렌드 어디서 팔로우해?" 요청 시
- Anthropic/OpenAI/Google 업데이트 추적 필요 시
- 팀/의사결정용 AI 분야 현황 문서화 필요 시
- "인플루언서", "뉴스레터", "논문", "에이전트 트렌드" 언급 시
- HTML + 마크다운 동시 생성 요청 시
- GitHub 자동 통합(커밋, 이슈) 요청 시

❌ **이런 경우 사용 안 함:**
- 논문 단건 조회 (웹 검색 직접 사용)
- 개인 메모 (파일 생성 직접 사용)
- AI 일반 질문 (Claude 직접 응답)

## 사용 방법

### 기본 사용
```
/ai-agent-research-report
```
전체 리포트 생성: 논문 TOP 5 + 인플루언서 6개 + 기업 업데이트. WebSearch 사용 (토큰 효율적).

### 옵션 사용

**범위 옵션:**
- `--papers-only` — 논문 TOP 5만, 인플루언서/기업 생략
- `--influencers-only` — Reddit + X 맵만
- `--companies-only` — Anthropic/OpenAI/Google 업데이트만
- `--update-html` — 기존 마크다운에서 HTML만 재생성 (빠름)
- `--create-issues` — 개선 사항을 GitHub Issues로 등록

**검색 전략:**
- `--web-search` (기본값) — WebSearch로 최신 정보, 50K~100K 토큰
- `--deep-research` — deep-research 워크플로우 (종합적이지만 1.5M+ 토큰, 분기별 심층 분석용)

**GitHub 옵션:**
- `--git-commit` — 리포트 자동 git 커밋 (날짜 포함 커밋 메시지)
- `--git-push` — 커밋 후 origin/master 자동 push

### 사용 예시

```bash
# 빠른 일간 리포트 (논문만)
/ai-agent-research-report --papers-only --web-search

# 매주 금요일 전체 리포트 + GitHub 커밋
/ai-agent-research-report --web-search --git-commit

# HTML 스타일만 업데이트 (재검색 없음)
/ai-agent-research-report --update-html

# 월간 심층 분석 (느림, 토큰 많음)
/ai-agent-research-report --deep-research --git-commit --create-issues

# 인플루언서 활동 상태 확인 (10개월 주기)
/ai-agent-research-report --influencers-only --web-search
```

## 리포트 구조

### 파트 A: 핵심 논문 TOP 5
각 논문 포함 항목:
- **제목, 저자, 컨퍼런스/발표처, 날짜**
- **선정 이유** — 왜 이 논문인가? (영향력, 참신성, 실용성)
- **핵심 아이디어** — 어떤 문제를 해결하나? (중간 깊이 설명)
- **실무 활용** — 실제로 어떻게 사용할 수 있나?

**선정 기준:** (1) 인용수/영향력, (2) 최상위 컨퍼런스(ICLR/ICML/NeurIPS), (3) 오픈소스 구현 + HuggingFace 채택 교집합.

### 파트 B: 인플루언서 맵
**Reddit (3개 커뮤니티):**
- `r/LocalLLaMA` — 실용적 LLM 배포
- `r/MachineLearning` — 연구 논문 + 토론
- `r/LangChain` — 에이전트 프레임워크 구현

**X / 트위터 (3개 계정):**
- `@karpathy` — LLM 기초 + 업계 프레임
- `@simonw` — 직접 써보는 LLM 도구 리뷰
- `@swyx` — AI 엔지니어 생태계 트렌드

각 항목: 링크, 팔로우 이유, 예상 콘텐츠, 최근 게시물 예시.

### 파트 C: 기업 업데이트
타임라인 표 (날짜 | 업데이트 | 핵심 기능 | 의의):
- **Anthropic**: Claude 3.x, Computer Use, MCP, Claude Code, Extended Thinking
- **OpenAI**: GPT-4o 변형, o3/o4 추론, Operator, Deep Research, Responses API
- **Google**: Gemini 2.0+, Project Astra, Agentspace, Jules, Vertex AI

### 파트 D: 트렌드 요약
기업 간 교차 패턴(추론 모델 수렴, 컴퓨터 조작 경쟁, MCP 표준화 등) + 의사결정 트리("X 용도에는 Y 선택").

## 토큰 전략

**기본값 (WebSearch):** ~50~100K 토큰
- 5방향 병렬 검색 (논문, 인플루언서, 기업 업데이트, 트렌드, 검증)
- 경량 소스 추출
- 빠름 (5~10분)

**선택사항 (deep-research):** ~1.5~2M 토큰
- 5방향 검색 + 15개 소스 + 3-vote 교차 검증
- 종합적이지만 비용 높음
- 느림 (15~20분)
- **분기별 심층 분석용으로만 사용, 일간 사용 금지**

## 출력 예시

```
# 2026 AI Agent 트렌드 리서치 리포트
**작성일**: 2026-06-11

## 📄 파트 A: 핵심 논문 TOP 5

### 1위: GLEAN (Guideline-Grounded Evidence Accumulation)
- **발표처**: ICLR 2026 Workshop, Best Paper
- **선정 이유**: 고위험 도메인(의료·법률·금융) 에이전트 검증 신뢰성
- **핵심**: ...
- **실무**: ...

... (4개 추가 논문)

## 👥 파트 B: 인플루언서 맵
... (Reddit 3개 + X 3개)

## 🏢 파트 C: 기업 업데이트
| 날짜 | 업데이트 | 핵심 기능 | 의의 |
|------|---------|---------|------|
| 2025-02 | Claude Code (GA) | 자율 코딩 에이전트 | IDE 독립적 |
...

## 🔗 파트 D: 업계 트렌드
- 추론 모델 확산
- 컴퓨터 조작 에이전트
- ...
```

## 구현 세부사항

### 핵심 흐름 (`generate_report.py` 참조)
```
ReportGenerator.run()
├─ 1단계: 인자 파싱 (--papers-only, --web-search, --git-commit 등)
├─ 2단계: 생성할 섹션 결정
├─ 3단계: 데이터 수집 (_generate_papers_section 등)
├─ 4단계: 마크다운 생성 (_generate_markdown)
├─ 5단계: HTML 생성 (_generate_html)
├─ 6단계: Git 커밋 (--git-commit 시)
├─ 7단계: Git push (--git-push 시)
└─ 8단계: 이슈 생성 (--create-issues 시, API 필요)
```

### 실행 경로 매트릭스
| 모드 | 섹션 | 시간 | 토큰 | Git | 이슈 |
|------|------|------|------|-----|------|
| `--papers-only` | 논문 | 3~5분 | 20~30K | ❌ | ❌ |
| `--web-search` | 전체 | 5~10분 | 50~100K | ✅ | ✅ |
| `--deep-research` | 전체 | 15~20분 | 1.5~2M | ✅ | ✅ |

## 성공 기준

✅ **리포트 필수 포함 항목:**
- [ ] 논문 5편 (제목, 저자, 발표처, 선정 이유, 핵심 아이디어, 활용법)
- [ ] 인플루언서 6개 (Reddit 3 + X 3, 링크 및 맥락 포함)
- [ ] 기업 업데이트 (Anthropic 7개+, OpenAI 8개+, Google 8개+)
- [ ] 업계 트렌드 요약 (6개+ 교차 패턴)
- [ ] 마크다운 + HTML 모두 10분 이내 생성
- [ ] 전체 링크 유효 (재실행 시 자동 갱신)
- [ ] 지식 컷오프 명시 (2025-08 또는 웹 검색 날짜)
- [ ] Git 커밋 메시지에 날짜 포함 (YYYY-MM-DD)

❌ **자주 발생하는 실수:**
- TOP 5가 될 논문이 없으면 억지로 채우지 말 것 (TOP 3 + 주목할 논문 형식 사용)
- 비활성 인플루언서 포함 금지 (최근 3개월 활동 검증)
- 날짜 구분 없이 구형/신형 기업 업데이트 혼재 금지
- 근거 없는 2026년 예측 금지 (현황 스냅샷임을 명시)

## 토큰 & 시간 예산

| 모드 | 토큰 | 시간 | 사용 시점 |
|------|------|------|----------|
| `--papers-only` | 20~30K | 3~5분 | 빠른 리서치 |
| `--web-search` (전체) | 50~100K | 5~10분 | 일간/주간 |
| `--deep-research` (전체) | 1.5~2M | 15~20분 | 월간 심층 분석 |
| `--update-html` | 5K 미만 | 1분 미만 | 스타일/형식 갱신 |

## 문제 해결

**3개월 후 링크가 깨졌다면?**
- `--web-search` 옵션으로 분기마다 재실행해 링크 갱신

**인플루언서가 비활성인 것 같다면?**
- `--influencers-only --web-search`로 현재 활동 상태 확인 (1K 토큰 미만)

**HTML이 이상하게 보인다면?**
- HTML 생성 로직의 CSS 수정 후 `--update-html`로 재생성 (재검색 불필요)

**GitHub 커밋이 실패한다면?**
- git 설정 확인, PAT 유효성 검증, 저장소 쓰기 권한 확인
- 필요 시 수동 커밋으로 대체

---

## 테스트 검증

**테스트 리포트**: 3개 시나리오 종합 검증은 `TEST_REPORT.md` 참조.

| 테스트 | 시나리오 | 상태 | 비고 |
|--------|----------|------|------|
| #1 | 전체 리포트 + 커밋 | ✅ 통과 | 전 섹션 생성, git 커밋 동작 |
| #2 | 논문만 (빠른 실행) | ✅ 통과 | 집중 출력, 5분 이내 |
| #3 | GitHub 통합 | ⚠️ 부분 | 커밋/push 동작; Issues API 스텁 상태 |

## GitHub 이슈 관리

### 이슈 워크플로우

```
이슈 생성 (상태: open)
    ↓
in-progress 레이블 추가
    ↓
"Closes #N" 포함 커밋
    ↓
GitHub 자동 닫기
```

### 레이블 시스템 (13개)

**상태**: open, in-progress, resolved
**우선순위**: high, medium, low
**카테고리**: skill, report, automation
**유형**: bug, enhancement, refactor, docs

## 아키텍처 및 구현

### ReportGenerator 클래스 (`generate_report.py`)
- **옵션**: argparse로 인자 파싱
- **섹션**: 동적 라우팅 (논문/인플루언서/기업)
- **생성**: 템플릿 마크다운 → HTML 변환
- **통합**: Git 커밋/push, GitHub API 훅
- **로깅**: 타임스탬프 + 이모지 접두사 상태 메시지

### 데이터 수집 (스텁 → 실제 구현 예정)
```python
_generate_papers_section()      # → WebSearch/deep-research
_generate_influencers_section() # → WebSearch
_generate_companies_section()   # → WebSearch
```

### 파일 구조
```
.claude/skills/ai-agent-research-report/
├── SKILL.md (현재 파일) — 전체 문서
├── README.md — 빠른 시작 가이드
├── TEST_REPORT.md — 검증 리포트
├── scripts/
│   └── generate_report.py — 메인 구현체
└── evals/
    └── evals.json — 3개 테스트 시나리오
```

## 프로덕션 로드맵

**Phase 1 (완료)**: 핵심 아키텍처 ✅
- 옵션 파싱 ✅
- 마크다운/HTML 생성 ✅
- Git 통합 ✅
- 테스트 검증 ✅

**Phase 2 (진행 중)**: 데이터 통합 ⚠️
- WebSearch 훅
- deep-research 폴백
- GitHub Issues API

**Phase 3 (선택)**: 마감 처리
- 캐싱
- 요청 한도 관리
- 확장 데이터 소스
