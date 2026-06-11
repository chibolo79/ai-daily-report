#!/usr/bin/env python3
"""
GitHub Issue Resolver
Fetches open issues, generates solution comments, posts them, and closes issues.
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from typing import Optional


def make_request(url: str, method: str, token: str, data: Optional[bytes] = None):
    """Make a GitHub API request with proper UTF-8 encoding."""
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"token {token}")
    req.add_header("User-Agent", "claude-github-issue-resolver")
    req.add_header("Accept", "application/vnd.github.v3+json")
    if data:
        req.add_header("Content-Type", "application/json; charset=utf-8")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {body}")


def fetch_open_issues(repo: str, token: str, state: str = "open") -> list:
    url = f"https://api.github.com/repos/{repo}/issues?state={state}&per_page=100"
    issues = make_request(url, "GET", token)
    # Filter out pull requests (GitHub API returns PRs in issues endpoint)
    return [i for i in issues if "pull_request" not in i]


def get_priority(labels: list) -> str:
    names = [l["name"] for l in labels]
    if "high-priority" in names:
        return "high"
    if "medium-priority" in names:
        return "medium"
    return "low"


def generate_comment(issue: dict) -> str:
    """
    Generate a solution comment for an issue.
    In real Claude-assisted usage, this is replaced by Claude's own analysis.
    This function provides a structured template as fallback.
    """
    title = issue.get("title", "")
    body = issue.get("body", "") or ""
    labels = issue.get("labels", [])
    priority = get_priority(labels)
    label_names = [l["name"] for l in labels]

    # Build a structured solution comment
    sections = ["## 해결 방안\n"]

    if priority == "high":
        sections.append(f"**우선순위가 높은 이슈입니다. 즉시 처리가 필요합니다.**\n")

    sections.append("### 문제 분석")
    if body.strip():
        sections.append(f"이슈 본문 분석:\n> {body[:300]}{'...' if len(body) > 300 else ''}\n")
    else:
        sections.append("이슈 본문이 없어 제목만으로 판단했습니다.\n")

    sections.append("### 해결 방법")
    sections.append("- 이슈에서 식별된 문제를 단계적으로 처리합니다.")
    sections.append("- 관련 코드/설정을 검토하고 수정합니다.")
    sections.append("- 변경사항을 테스트 후 적용합니다.\n")

    sections.append("### 적용 방법")
    sections.append("구체적인 구현은 다음 PR 또는 커밋에서 추적합니다.\n")

    if label_names:
        sections.append(f"**레이블**: {', '.join(f'`{l}`' for l in label_names)}")

    return "\n".join(sections)


def post_comment(repo: str, issue_num: int, comment: str, token: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"\n[DRY RUN] #{issue_num} 댓글 미리보기:\n{comment[:200]}...\n")
        return True

    url = f"https://api.github.com/repos/{repo}/issues/{issue_num}/comments"
    payload = json.dumps({"body": comment}, ensure_ascii=False).encode("utf-8")
    try:
        make_request(url, "POST", token, payload)
        return True
    except RuntimeError as e:
        print(f"  댓글 실패: {e}")
        return False


def close_issue(repo: str, issue_num: int, token: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"[DRY RUN] #{issue_num} 닫기 (실제 실행 안 함)")
        return True

    url = f"https://api.github.com/repos/{repo}/issues/{issue_num}"
    payload = json.dumps({"state": "closed"}, ensure_ascii=False).encode("utf-8")
    try:
        make_request(url, "PATCH", token, payload)
        return True
    except RuntimeError as e:
        print(f"  닫기 실패: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Resolve GitHub issues with solution comments")
    parser.add_argument("--repo", required=True, help="owner/repo (e.g. chibolo79/ai-daily-report)")
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--issues", nargs="*", type=int, help="Specific issue numbers to process")
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"])
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    parser.add_argument("--no-close", action="store_true", help="Post comments but don't close issues")
    args = parser.parse_args()

    print(f"저장소: {args.repo}")
    print(f"모드: {'DRY RUN' if args.dry_run else '실제 실행'}\n")

    # Fetch issues
    try:
        issues = fetch_open_issues(args.repo, args.token, args.state)
    except RuntimeError as e:
        print(f"이슈 조회 실패: {e}")
        sys.exit(1)

    if args.issues:
        issues = [i for i in issues if i["number"] in args.issues]

    if not issues:
        print("처리할 이슈가 없습니다.")
        sys.exit(0)

    print(f"처리할 이슈 {len(issues)}개:\n")
    for issue in issues:
        labels = [l["name"] for l in issue.get("labels", [])]
        print(f"  #{issue['number']}: {issue['title']} [{', '.join(labels)}]")

    print()
    results = {"success": [], "failed": []}

    for issue in issues:
        num = issue["number"]
        title = issue["title"]
        print(f"처리 중: #{num} {title}")

        comment = generate_comment(issue)
        comment_ok = post_comment(args.repo, num, comment, args.token, args.dry_run)

        close_ok = True
        if not args.no_close:
            close_ok = close_issue(args.repo, num, args.token, args.dry_run)

        if comment_ok and close_ok:
            results["success"].append(num)
            print(f"  ✅ 완료")
        else:
            results["failed"].append(num)
            print(f"  ❌ 일부 실패")

        # Respect rate limits
        time.sleep(0.5)

    print(f"\n--- 결과 ---")
    print(f"성공: {len(results['success'])}개 {results['success']}")
    print(f"실패: {len(results['failed'])}개 {results['failed']}")
    print(f"\n확인: https://github.com/{args.repo}/issues")


if __name__ == "__main__":
    main()
