---
name: github-issue-resolver
description: Resolve open GitHub issues by posting structured solution comments and closing them via the GitHub API. Use this skill whenever the user wants to: triage or close GitHub issues, add solution/fix comments to issues, bulk-resolve multiple open issues, continue work from a GitHub issue list, work through a backlog of open issues, or says things like "이슈 해결해줘", "이슈에 댓글 달고 닫아줘", "GitHub 이슈 처리해줘", "resolve issues", "close issues with comments", "이슈 작업 이어서 하고 싶어". Trigger even when the user just pastes a GitHub issues URL and says they want to continue working.
---

## What This Skill Does

Reads open GitHub issues from a repository, generates structured solution comments for each one, posts the comments via the GitHub API, and closes the issues — all in one automated workflow.

**Typical use case:** The user has a backlog of open issues (bugs, improvements, feature requests) and wants Claude to analyze each one, propose a resolution, post it as a comment, and mark it resolved.

## Setup: GitHub Token

A Personal Access Token (PAT) with `repo` scope is required to post comments and close issues.

**Priority order for finding the token:**
1. `$env:GITHUB_TOKEN` or `$env:GH_TOKEN` environment variable
2. User provides it directly in the conversation
3. Ask the user — direct them to: GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic) → check `repo` scope

**Important:** Never log the token. Store it only in a local variable for the duration of the session.

## Workflow

### Step 1: Identify the repository

Extract `owner/repo` from:
- A GitHub URL the user provided (e.g., `https://github.com/owner/repo/issues`)
- The current git remote: run `git remote get-url origin` and parse it
- Explicit user input

### Step 2: Fetch open issues

Call the GitHub API to list open issues. Use the script at `scripts/resolve_issues.py` or call the API directly via PowerShell/curl.

```
GET https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=100
```

Display the list to the user before proceeding:
```
오픈 이슈 N개를 발견했습니다:
- #14: 자동화 계획 미성숙 [high-priority]
- #12: 기업 업데이트 불완전 [medium-priority]
...
모두 처리할까요, 아니면 특정 이슈만 처리할까요?
```

### Step 3: Generate solution comments

For each issue, read its `title`, `body`, and `labels`, then write a solution comment that includes:

```markdown
## 해결 방안

**[한 줄 요약 — 핵심 해결 접근법]**

### 문제 분석
[이슈 본문을 바탕으로 근본 원인 설명]

### 해결 방법
[구체적인 조치 항목 — 코드 변경, 설정 수정, 워크플로우 개선 등]

### 적용 방법
[실제로 어떻게 구현하는지 — 명령어, 파일명, 함수명 포함]

### 우선순위 / 일정
[언제, 어떤 순서로 처리할지]
```

Tailor the depth to the issue's priority label:
- `high-priority`: thorough analysis with code examples or config snippets
- `medium-priority`: clear steps, moderate detail
- `low-priority`: concise bullet points

### Step 4: Post comment + close issue

For each issue, use UTF-8 encoded API calls (critical for Korean text):

```python
# See scripts/resolve_issues.py for the reference implementation
headers = {"Authorization": f"token {token}", "User-Agent": "claude-agent"}
body = json.dumps({"body": comment_text}, ensure_ascii=False).encode("utf-8")

# Post comment
requests.post(f"https://api.github.com/repos/{repo}/issues/{num}/comments",
              headers=headers, data=body,
              headers={**headers, "Content-Type": "application/json; charset=utf-8"})

# Close issue
requests.patch(f"https://api.github.com/repos/{repo}/issues/{num}",
               data=json.dumps({"state": "closed"}, ensure_ascii=False).encode("utf-8"), ...)
```

**UTF-8 encoding is mandatory** — GitHub API will return `400 Problems parsing JSON` if Korean characters are passed as default-encoded strings in PowerShell.

### Step 5: Report results

After processing all issues, summarize:

```
완료 결과:
✅ #14 자동화 계획 미성숙 — 댓글 추가 + 닫기 완료
✅ #12 기업 업데이트 불완전 — 댓글 추가 + 닫기 완료
❌ #11 실패: [에러 메시지]

총 N개 중 M개 처리 완료.
링크: https://github.com/{owner}/{repo}/issues
```

## Using the Script

`scripts/resolve_issues.py` handles the full workflow. Run it from the project root:

```bash
# Process all open issues
python .claude/skills/github-issue-resolver/scripts/resolve_issues.py \
  --repo owner/repo \
  --token ghp_xxx

# Dry run — show what comments would be posted, but don't actually post
python .claude/skills/github-issue-resolver/scripts/resolve_issues.py \
  --repo owner/repo \
  --token ghp_xxx \
  --dry-run

# Process specific issues only
python .claude/skills/github-issue-resolver/scripts/resolve_issues.py \
  --repo owner/repo \
  --token ghp_xxx \
  --issues 14 12 11
```

## Edge Cases

**Issue is a question, not a bug/task:**
Close with a comment that answers the question directly. Label it `answered` if that label exists.

**Issue has no body:**
Base the solution comment entirely on the title. Note "이슈 본문이 없어 제목만으로 판단했습니다."

**API rate limit (403):**
Wait 60 seconds, then retry. The GitHub API allows 5000 requests/hour for authenticated users.

**Issue is already closed:**
Skip it. Log: `#N already closed, skipping.`

**Issue has linked PRs:**
Mention the PR in the comment: "관련 PR #X 가 이미 생성되어 있습니다."

## Options Summary

| Flag | Effect |
|------|--------|
| `--dry-run` | Generate comments without posting them |
| `--issues N [N...]` | Process only specified issue numbers |
| `--state open\|closed\|all` | Which issues to fetch (default: open) |
| `--lang ko\|en` | Comment language (default: matches issue body language) |
| `--no-close` | Post comments but don't close issues |

## Security Note

The GitHub token grants write access to the repository. Confirm the `owner/repo` with the user before making any API calls, especially before closing issues. Never commit the token to version control.
