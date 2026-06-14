# AI Daily Report

AI Agent 분야 논문·인플루언서·기업 업데이트를 Claude가 자동 수집·정리하는 프로젝트.  
→ 미션·설계 원칙: [SOUL.md](SOUL.md) | Claude 행동 지침: [CLAUDE.md](CLAUDE.md)

## Structure

```
.
├── SOUL.md                          # 미션·설계 원칙
├── README.md                        # 이 파일 — 구조·빠른 시작
├── CLAUDE.md                        # Claude Code 행동 지침
├── ISSUES.md                                    # 신규 약점 임시 보관 (GitHub 등록 후 삭제)
├── 2026-06-11_AI_Agent_Research_Report.md       # 최신 리포트 (마크다운)
├── 2026-06-11_AI_Agent_Research_Report.html     # 최신 리포트 (HTML)
└── .claude/skills/
    ├── ai-agent-research-report/    # AI 리서치 리포트 생성 스킬
    ├── github-issue-resolver/       # GitHub 이슈 해결 스킬
    ├── briefing-improver/           # 전체 개선 사이클 스킬
    ├── doc-optimizer/               # 문서 최적화 스킬
    └── vietnam-visit-report/        # 베트남 출장 방문 보고서 스킬
```

## Quick Start

```bash
# 전체 리포트 (WebSearch)
python .claude/skills/ai-agent-research-report/scripts/generate_report.py --web-search

# 논문만 (빠른 조회)
python .claude/skills/ai-agent-research-report/scripts/generate_report.py --papers-only

# 생성 후 커밋
python .claude/skills/ai-agent-research-report/scripts/generate_report.py --web-search --git-commit
```

## Recommended Schedule

| 주기 | 작업 | 옵션 | 토큰 |
|------|------|------|------|
| 매일 | 논문 헤드라인 | `--papers-only` | ~20-30K |
| 매주 | 전체 리포트 | `--web-search --git-commit` | ~50-100K |
| 매월 | 갱신 + 푸시 | `--web-search --git-commit --git-push` | ~50-100K |
| 분기 | 심층 분석 | `--deep-research --git-commit --git-push --create-issues` | ~1.5-2M |

→ 전체 옵션: [ai-agent-research-report/SKILL.md](.claude/skills/ai-agent-research-report/SKILL.md)  
→ 이슈 자동 처리: [github-issue-resolver/SKILL.md](.claude/skills/github-issue-resolver/SKILL.md)  
→ 전체 개선 사이클: [briefing-improver/SKILL.md](.claude/skills/briefing-improver/SKILL.md)

## Requirements

- Python 3.8+, Git
- GitHub PAT (`repo` scope) — 커밋·이슈 기능 사용 시
