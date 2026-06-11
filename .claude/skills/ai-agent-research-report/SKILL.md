---
name: ai-agent-research-report
description: Generate comprehensive AI Agent trend reports with latest research papers, influencer recommendations, and company updates. Use this skill whenever the user wants to create, update, or analyze AI Agent research reports, track latest LLM/Agent publications, find influential voices in AI engineering, or maintain current information about Anthropic/OpenAI/Google developments. Also use when the user mentions "AI report", "research paper trends", "influencer map", "agent updates", or wants to document AI field progress for reference or sharing.
compatibility: Requires WebFetch, Grep, Write tools; optionally uses deep-research skill for comprehensive analysis
---

## What This Skill Does

Generates a complete **2026 AI Agent Research Report** containing:

1. **TOP 5 Research Papers** — Latest AI Agent papers ranked by impact, conference tier, and practical applicability
2. **Influencer Map** — 6 recommended voices (3 Reddit communities + 3 X accounts) with context on why follow each
3. **Company Updates Timeline** — Anthropic, OpenAI, Google agent/LLM releases with technical details
4. **Industry Trends** — Cross-company patterns and technology selection guide

**Output formats:**
- Markdown (`YYYY-MM-DD_AI_Agent_Research_Report.md`)
- HTML (`YYYY-MM-DD_AI_Agent_Research_Report.html`)
- Optional: GitHub commits + Issues tracking improvements

## When to Use This Skill

✅ **Use this skill when:**
- User wants "AI Agent report" or "2026 AI research summary"
- User asks "which papers should I read on LLM agents?"
- User requests "where can I follow AI trends?"
- User wants to track Anthropic/OpenAI/Google updates
- User needs to document current state of AI field for team/decision-making
- User mentions "influencer", "newsletter", "research paper", "agent trends"
- User wants HTML + markdown versions of reports simultaneously
- User requests automatic GitHub integration (commits, issues)

❌ **Don't use this skill for:**
- Single paper lookup (use web search directly)
- Personal note-taking (use file creation directly)
- General questions about AI (use Claude directly)

## How to Use

### Basic Usage
```
/ai-agent-research-report
```
Generates full report: TOP 5 papers + 6 influencers + company updates. Uses WebSearch (token-efficient).

### With Options

**Scope options:**
- `--papers-only` — TOP 5 papers only, skip influencers/companies
- `--influencers-only` — Reddit + X map only
- `--companies-only` — Anthropic/OpenAI/Google updates only
- `--update-html` — Regenerate HTML from existing markdown (fast)
- `--create-issues` — Register identified improvements as GitHub Issues

**Search strategy:**
- `--web-search` (default) — WebSearch for current info, 50K-100K tokens
- `--deep-research` — Use deep-research workflow (comprehensive but 1.5M+ tokens, only for quarterly deep-dives)

**GitHub options:**
- `--git-commit` — Auto-commit report to git (includes date in commit message)
- `--git-push` — Auto-push to origin/master after commit

### Examples

```
# Quick daily report (papers only)
/ai-agent-research-report --papers-only --web-search

# Full Friday report with GitHub commit
/ai-agent-research-report --web-search --git-commit

# Update HTML styling only (no new research)
/ai-agent-research-report --update-html

# Monthly deep-dive (slow, token-heavy)
/ai-agent-research-report --deep-research --git-commit --create-issues

# Influencer verification (10-month activity check)
/ai-agent-research-report --influencers-only --web-search
```

## Report Structure

### Part A: TOP 5 Papers
Each paper includes:
- **Title, authors, conference/venue, date**
- **Selection rationale** — Why this paper? (impact, novelty, practical use)
- **Core idea** — What problem does it solve? (medium-depth explanation)
- **Real-world application** — How would you actually use this?

**Ranking criteria:** Intersection of (1) citations/impact, (2) top-tier venue (ICLR/ICML/NeurIPS), (3) open-source implementation + HuggingFace adoption.

### Part B: Influencer Map
**Reddit (3 communities):**
- `r/LocalLLaMA` — Practical LLM deployment
- `r/MachineLearning` — Research papers + discussion
- `r/LangChain` — Agent framework implementation

**X / Twitter (3 accounts):**
- `@karpathy` — LLM fundamentals + industry frames
- `@simonw` — Hands-on LLM tool reviews
- `@swyx` — AI Engineer ecosystem trends

For each: link, why follow, what to expect, example recent posts.

### Part C: Company Updates
Timeline table (date | update | core feature | significance) for:
- **Anthropic**: Claude 3.x, Computer Use, MCP, Claude Code, Extended Thinking
- **OpenAI**: GPT-4o variants, o3/o4 reasoning, Operator, Deep Research, Responses API
- **Google**: Gemini 2.0+, Project Astra, Agentspace, Jules, Vertex AI

### Part D: Trends Summary
Cross-company patterns (e.g., reasoning model convergence, computer-use race, MCP standardization) + decision tree ("choose X for Y use case").

## Token Strategy

**Default (WebSearch):** ~50-100K tokens
- 5 parallel searches (papers, influencers, company updates, trends, verification)
- Lightweight source extraction
- Fast (5-10 min)

**Optional (deep-research):** ~1.5-2M tokens
- 5-direction search + 15 sources + 3-vote verification
- Comprehensive but expensive
- Slow (15-20 min)
- **Use only for quarterly deep-dives, not daily**

## Output Example

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

## Success Criteria

✅ **Report must have:**
- [ ] 5 papers with selection rationale + core idea + application
- [ ] 6 influencers (Reddit 3 + X 3) with context
- [ ] Company updates: Anthropic (7+ items), OpenAI (8+ items), Google (8+ items)
- [ ] Industry trends summary (6+ patterns)
- [ ] Both markdown + HTML generated
- [ ] All links are valid (spot-check 5 random links)
- [ ] Knowledge cutoff clearly stated (2025-08 or web-search date if used)

❌ **Common issues to avoid:**
- Don't force TOP 5 if fewer papers deserve it (better to say "TOP 3 + honorable mentions")
- Don't include inactive influencers (verify last 3 months activity)
- Don't mix old company updates with new ones without date clarity
- Don't make claims about 2026 predictions without caveat (this is a snapshot, not forecast)

## Token & Time Budgets

| Mode | Tokens | Time | Use Case |
|------|--------|------|----------|
| `--papers-only` | 20-30K | 3-5 min | Quick research |
| `--web-search` (full) | 50-100K | 5-10 min | Daily/weekly |
| `--deep-research` (full) | 1.5-2M | 15-20 min | Monthly deep-dive |
| `--update-html` | <5K | <1 min | Style/format refresh |

## Troubleshooting

**Links broken after 3 months?**
- Re-run with `--web-search` quarterly to refresh all links

**Influencers seem inactive?**
- Re-run with `--influencers-only --web-search` to verify current activity (takes <1K tokens)

**HTML looks ugly?**
- Adjust CSS in the HTML generation logic; save to `--update-html` to regenerate without re-researching

**GitHub commit fails?**
- Check git config, verify PAT is valid, ensure repo is writable
- Fall back to manual commit if needed

---

## GitHub Issues Management

### Issue Workflow

```
Issue Created (status: open)
    ↓
Work on solution (add status: in-progress label)
    ↓
Commit with "Closes #N" (status: resolved)
    ↓
Issue auto-closed on GitHub
```

### Available Labels

**Status:**
- `status/open` — Investigating
- `status/in-progress` — Being worked on  
- `status/resolved` — Completed

**Priority:**
- `priority/high` — Do immediately
- `priority/medium` — Next cycle
- `priority/low` — Long-term improvement

**Category:**
- `category/skill` — Skill implementation
- `category/report` — Report content
- `category/automation` — Automation workflow

### Auto-Close Issues

When committing a fix, include in message:

```bash
git commit -m "Update automation strategy

- Change frequency from daily to weekly
- Reduce token budget to 50-100K

Closes #14"
```

## Implementation Notes

This skill:
1. Uses **WebSearch (default)** or **deep-research (quarterly)** to gather data
2. **Deduplicates and ranks** findings (papers by impact, influencers by activity, updates by date)
3. **Generates markdown** with structured sections
4. **Converts markdown to HTML** with CSS styling (gradient header, responsive tables)
5. **Optionally commits + pushes** to GitHub with date-stamped message
6. **Optionally creates Issues** for identified gaps with proper GitHub labels
7. **Manages issue workflow** with status labels and auto-close on commit

**Files:**
- `README.md` — Quick start guide, examples, troubleshooting
- `scripts/generate_report.py` — Main implementation
- `evals/evals.json` — Test cases (3 scenarios: full, quick, GitHub-integrated)
