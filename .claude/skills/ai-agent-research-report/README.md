# AI Agent Research Report Skill

**Generate comprehensive AI Agent trend reports with latest research papers, influencer recommendations, and company updates.**

## Quick Start

```bash
# Generate full report (WebSearch, 50-100K tokens)
python scripts/generate_report.py

# Generate papers only (fast, 20-30K tokens)
python scripts/generate_report.py --papers-only

# Auto-commit to GitHub
python scripts/generate_report.py --git-commit --git-push
```

## Features

✅ **TOP 5 Research Papers** — Latest AI Agent papers with selection rationale and practical applications  
✅ **Influencer Map** — 6 recommended voices (3 Reddit communities + 3 X accounts)  
✅ **Company Updates** — Anthropic, OpenAI, Google agent/LLM releases with technical details  
✅ **Dual Output** — Both Markdown and HTML formats generated simultaneously  
✅ **Token Efficient** — WebSearch (50-100K) by default, deep-research (1.5-2M) for quarterly deep-dives  
✅ **Git Integration** — Auto-commit and push with date-stamped messages  
✅ **Issues Tracking** — Automatically create GitHub issues for identified improvements  

## Token Strategy

| Mode | Tokens | Use Case | Frequency |
|------|--------|----------|-----------|
| `--papers-only` | 20-30K | Quick lookup | Daily |
| `--web-search` (default) | 50-100K | Full report | Weekly/Monthly |
| `--deep-research` | 1.5-2M | Comprehensive analysis | Quarterly |

**Bottom line:** Default (WebSearch) reduces tokens **20x** compared to deep-research.

## All Options

### Scope
- `--papers-only` — TOP 5 papers only
- `--influencers-only` — Reddit + X map only
- `--companies-only` — Company updates only

### Search Strategy
- `--web-search` (default) — Efficient web search (50-100K tokens)
- `--deep-research` — Comprehensive analysis (1.5-2M tokens, quarterly only)

### Output & Integration
- `--update-html` — Regenerate HTML from existing markdown (fast, <5K tokens)
- `--git-commit` — Auto-commit report to git
- `--git-push` — Auto-push to origin/master
- `--create-issues` — Register identified improvements as GitHub issues
- `--output-dir` — Custom output directory

## Usage Examples

### Recommended Workflows

**📌 Daily (08:00) — Quick Headlines**
```bash
python scripts/generate_report.py --papers-only --web-search
# Tokens: ~5K
# Time: ~3 minutes
```

**📌 Weekly (Monday) — Full Report**
```bash
python scripts/generate_report.py --web-search --git-commit
# Tokens: 50-100K
# Time: ~5-10 minutes
```

**📌 Monthly (End of Month) — Complete Update**
```bash
python scripts/generate_report.py --web-search --git-commit --git-push
# Tokens: 50-100K
# Time: ~5-10 minutes
```

**📌 Quarterly (Every 3 Months) — Deep Analysis**
```bash
python scripts/generate_report.py --deep-research --git-commit --git-push --create-issues
# Tokens: 1.5-2M
# Time: ~15-20 minutes
```

### GitHub Issues Management

Commits automatically close related issues:

```bash
# Commit that resolves issue #14
git commit -m "Update automation strategy for weekly reports

Closes #14"
```

**GitHub Labels** (automatically added):
- `status/open` — Investigating
- `status/in-progress` — Being worked on
- `status/resolved` — Completed
- `priority/high|medium|low` — Urgency
- `category/skill|report|automation` — Type

## Output Examples

### Markdown
```
2026-06-11_AI_Agent_Research_Report.md
├─ TOP 5 Papers (with rationale, core ideas, applications)
├─ Influencer Map (Reddit 3 + X 3)
├─ Company Updates (Anthropic, OpenAI, Google timeline)
└─ Industry Trends (cross-company patterns)
```

### HTML
```
2026-06-11_AI_Agent_Research_Report.html
└─ Styled version with tables, gradients, responsive design
```

## Directory Structure

```
.claude/skills/ai-agent-research-report/
├── SKILL.md                    # Skill documentation
├── README.md                   # This file
├── scripts/
│   ├── generate_report.py      # Main orchestrator
│   ├── search_papers.py        # Paper collection (stub)
│   ├── search_influencers.py   # Influencer mapping (stub)
│   └── search_company_updates.py # Company updates (stub)
├── evals/
│   └── evals.json              # Test cases
└── references/
    ├── paper_schema.json       # Data schema
    └── influencer_schema.json  # Data schema
```

## Troubleshooting

**Q: Links broken after 3 months?**
> A: Re-run with `--web-search` quarterly to refresh all links

**Q: Want influencer verification?**
> A: Run `python scripts/generate_report.py --influencers-only --web-search` (takes <1K tokens)

**Q: HTML looks plain?**
> A: Adjust CSS in `generate_report.py` markdown_to_html section, then run with `--update-html`

**Q: Git commit failed?**
> A: Check git config, verify GitHub token is valid, ensure repo is writable

## Performance Metrics

**Benchmarks (estimated):**
- Markdown generation: <1 sec
- HTML generation: <1 sec
- WebSearch (web mode): 5-10 min
- deep-research (quarterly mode): 15-20 min
- Git operations: <1 sec

**Token budgets:**
- Papers-only: 20-30K
- Full report (WebSearch): 50-100K
- Full report (deep-research): 1.5-2M

## Issue Resolution History

✅ **#9 — Token Waste** (RESOLVED)
- Implemented WebSearch as default (20x reduction)
- Added deep-research option for quarterly only
- Documented token budgets per mode

---

**Created:** 2026-06-11  
**Last Updated:** 2026-06-11  
**Status:** Active Development
