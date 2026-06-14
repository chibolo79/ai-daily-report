# AI Daily Report

AI 리서치 리포트 자동화 + 해외 영업 보고서 누적 관리를 Claude가 수행하는 프로젝트.  
→ 미션·설계 원칙: [SOUL.md](SOUL.md) | Claude 행동 지침: [CLAUDE.md](CLAUDE.md)

## Structure

```
.
├── SOUL.md                                        # 미션·설계 원칙
├── README.md                                      # 이 파일 — 구조·빠른 시작
├── CLAUDE.md                                      # Claude Code 행동 지침
├── ISSUES.md                                      # 신규 약점 임시 보관 (GitHub 등록 후 삭제)
├── 2026-06-11_AI_Agent_Research_Report.md         # AI 리서치 리포트 (마크다운)
├── 2026-06-11_AI_Agent_Research_Report.html       # AI 리서치 리포트 (HTML)
├── 2026-06-14_Oristar_Vietnam_Sales_Analysis.md   # 베트남 Oristar 대리점 세일즈 분석 (누적)
├── .claude/skills/
│   ├── ai-agent-research-report/    # AI 리서치 리포트 생성 스킬
│   ├── github-issue-resolver/       # GitHub 이슈 해결 스킬
│   ├── briefing-improver/           # 전체 개선 사이클 스킬
│   ├── doc-optimizer/               # 문서 최적화 스킬
│   └── vietnam-visit-report/        # 베트남 출장 방문 보고서 스킬
└── .claude/agents/
    ├── orchestrator.md              # 전체 워크플로우 조율 팀 리더
    ├── research-agent.md            # 논문·트렌드·인플루언서 웹 수집
    ├── report-writer-agent.md       # 마크다운/HTML 리포트 작성
    ├── github-agent.md              # GitHub 이슈 생성·댓글·닫기
    ├── doc-optimizer-agent.md       # CLAUDE.md·SOUL.md·README.md 정리
    ├── validator-agent.md           # 17항목 100점 루브릭 채점·등급 판정
    └── vietnam-sales-updater.md     # 베트남 세일즈 분석 파일 업데이트 전담
```

## Quick Start

### AI 리서치 리포트
```bash
# 전체 리포트 (WebSearch)
python .claude/skills/ai-agent-research-report/scripts/generate_report.py --web-search

# 논문만 (빠른 조회)
python .claude/skills/ai-agent-research-report/scripts/generate_report.py --papers-only

# 생성 후 커밋
python .claude/skills/ai-agent-research-report/scripts/generate_report.py --web-search --git-commit
```

### 베트남 출장 보고서
```
/vietnam-visit-report
```
출장 후 방문 내용(미팅 업체·담당자·논의 사항)을 입력하면 Claude가 기존 분석 파일에 누적 업데이트하고 커밋·푸시까지 처리.  
→ 분석 파일: [2026-06-14_Oristar_Vietnam_Sales_Analysis.md](2026-06-14_Oristar_Vietnam_Sales_Analysis.md)  
→ 스킬 상세: [vietnam-visit-report/SKILL.md](.claude/skills/vietnam-visit-report/SKILL.md)

## Recommended Schedule

### AI 리서치 리포트
| 주기 | 작업 | 옵션 | 토큰 |
|------|------|------|------|
| 매일 | 논문 헤드라인 | `--papers-only` | ~20-30K |
| 매주 | 전체 리포트 | `--web-search --git-commit` | ~50-100K |
| 매월 | 갱신 + 푸시 | `--web-search --git-commit --git-push` | ~50-100K |
| 분기 | 심층 분석 | `--deep-research --git-commit --git-push --create-issues` | ~1.5-2M |

### 베트남 출장 보고서
| 시점 | 작업 |
|------|------|
| 출장 전 | 잠재 고객 리스트 검토, 방문 체크포인트 확인 |
| 출장 후 | `/vietnam-visit-report`로 미팅 내용 입력 → 누적 문서 업데이트 → 커밋·푸시 |

→ 전체 옵션: [ai-agent-research-report/SKILL.md](.claude/skills/ai-agent-research-report/SKILL.md)  
→ 이슈 자동 처리: [github-issue-resolver/SKILL.md](.claude/skills/github-issue-resolver/SKILL.md)  
→ 전체 개선 사이클: [briefing-improver/SKILL.md](.claude/skills/briefing-improver/SKILL.md)

## Requirements

- Python 3.8+, Git
- GitHub PAT (`repo` scope) — 커밋·푸시·이슈 기능 사용 시
- 로컬 Work 디렉토리 (`C:\Work\`) — 출장 DOCX·XLSX 원본 파일 참조 시
