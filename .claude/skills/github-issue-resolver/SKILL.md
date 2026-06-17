---
name: github-issue-resolver
description: GitHub 오픈 이슈에 구조화된 해결 방안 댓글을 달고 이슈를 닫는 스킬. 사용자가 GitHub 이슈를 처리하고 싶을 때, 이슈에 해결 댓글을 달고 싶을 때, 여러 이슈를 한꺼번에 정리할 때 반드시 사용. "이슈 해결해줘", "이슈에 댓글 달고 닫아줘", "GitHub 이슈 처리해줘", "이슈 작업 이어서 하고 싶어", "resolve issues", "close issues with comments" 등의 표현에 트리거. 사용자가 GitHub issues URL을 붙여넣고 작업을 이어가겠다고 할 때도 즉시 트리거.
---

## 이 스킬이 하는 일

저장소의 오픈 이슈를 조회하고, 각 이슈에 맞는 해결 방안 댓글을 생성해 GitHub API로 게시한 뒤 이슈를 닫습니다. 전 과정을 자동화된 워크플로우로 처리합니다.

**전형적인 사용 상황:** 버그, 개선 제안, 기능 요청 등의 미처리 이슈가 쌓여 있을 때, Claude가 각 이슈를 분석해 해결안을 댓글로 달고 완료 처리합니다.

---

## 사전 준비: GitHub 토큰

댓글 게시 및 이슈 닫기에는 `repo` 권한이 있는 Personal Access Token(PAT)이 필요합니다.

**환경 주의**: 이 프로젝트는 Windows 환경이며 `gh` CLI가 설치되어 있지 않음. 모든 GitHub API 호출은 PowerShell + Python 스크립트 방식으로 처리한다. `git push`는 Windows Credential Manager로 자동 인증되지만, GitHub API(이슈·댓글)는 PAT가 별도로 필요하다.

**토큰 확인 순서:**
1. 환경변수 `$env:GITHUB_TOKEN` 또는 `$env:GH_TOKEN` 확인
2. 사용자가 대화에서 직접 입력
3. 없으면 발급 안내: GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → `repo` 체크

**주의:** 토큰은 로그에 출력하지 않는다. 세션 내 지역 변수로만 사용한다.

---

## 워크플로우

### 1단계: 저장소 식별

`owner/repo` 형식을 다음 순서로 파악한다:
- 사용자가 제공한 GitHub URL (예: `https://github.com/owner/repo/issues`)
- 현재 git 리모트: `git remote get-url origin` 실행 후 파싱
- 사용자 직접 입력

### 2단계: 오픈 이슈 조회

GitHub API로 오픈 이슈 목록을 가져온다. `scripts/resolve_issues.py` 스크립트를 사용하거나 PowerShell로 직접 호출한다.

```
GET https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=100
```

처리 전에 반드시 목록을 사용자에게 보여준다:
```
오픈 이슈 N개를 발견했습니다:
- #14: 자동화 계획 미성숙 [high-priority]
- #12: 기업 업데이트 불완전 [medium-priority]
...
모두 처리할까요, 아니면 특정 이슈만 처리할까요?
```

### 3단계: 해결 방안 댓글 작성

각 이슈의 `title`, `body`, `labels`를 읽고 아래 형식으로 댓글을 작성한다:

```markdown
## 해결 방안

**[한 줄 요약 — 핵심 해결 접근법]**

### 문제 분석
[이슈 본문을 바탕으로 근본 원인 설명]

### 해결 방법
[구체적인 조치 항목 — 코드 변경, 설정 수정, 워크플로우 개선 등]

### 적용 방법
[실제 구현 방법 — 명령어, 파일명, 함수명 포함]

### 우선순위 / 일정
[언제, 어떤 순서로 처리할지]
```

우선순위 레이블에 따라 댓글 깊이를 조절한다:
- `high-priority`: 코드 예시·설정 스니펫 포함한 상세 분석
- `medium-priority`: 명확한 단계별 설명, 중간 수준 상세도
- `low-priority`: 간결한 불릿 포인트

### 4단계: 댓글 게시 + 이슈 닫기

한국어 텍스트가 포함되므로 **UTF-8 인코딩이 필수**다. 기본 인코딩으로 전송하면 GitHub API가 `400 Problems parsing JSON`을 반환한다.

```python
# scripts/resolve_issues.py 참고
import json, urllib.request

headers = {
    "Authorization": f"token {token}",
    "User-Agent": "claude-agent",
    "Content-Type": "application/json; charset=utf-8",
}

# 댓글 게시
payload = json.dumps({"body": comment_text}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/issues/{num}/comments",
    data=payload, method="POST", headers=headers
)
urllib.request.urlopen(req)

# 이슈 닫기
close_payload = json.dumps({"state": "closed"}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/issues/{num}",
    data=close_payload, method="PATCH", headers=headers
)
urllib.request.urlopen(req)
```

### 5단계: 결과 보고

모든 이슈 처리 후 요약한다:

```
완료 결과:
✅ #14 자동화 계획 미성숙 — 댓글 추가 + 닫기 완료
✅ #12 기업 업데이트 불완전 — 댓글 추가 + 닫기 완료
❌ #11 실패: [에러 메시지]

총 N개 중 M개 처리 완료.
확인: https://github.com/{owner}/{repo}/issues
```

---

## 스크립트 사용법

`scripts/resolve_issues.py`로 전체 워크플로우를 실행한다. 프로젝트 루트에서 실행:

```bash
# 전체 오픈 이슈 처리
python .claude/skills/github-issue-resolver/scripts/resolve_issues.py \
  --repo owner/repo \
  --token ghp_xxx

# 미리보기 (실제 게시 안 함)
python .claude/skills/github-issue-resolver/scripts/resolve_issues.py \
  --repo owner/repo \
  --token ghp_xxx \
  --dry-run

# 특정 이슈만 처리
python .claude/skills/github-issue-resolver/scripts/resolve_issues.py \
  --repo owner/repo \
  --token ghp_xxx \
  --issues 14 12 11
```

---

## 예외 처리

**이슈가 질문 형식인 경우:**
질문에 직접 답변하는 댓글을 달고 닫는다. `answered` 레이블이 있으면 추가한다.

**이슈 본문이 없는 경우:**
제목만으로 해결안을 작성하고 "이슈 본문이 없어 제목만으로 판단했습니다."를 명시한다.

**API 요청 한도 초과 (403):**
60초 대기 후 재시도한다. 인증된 사용자는 시간당 5000회 요청 가능.

**이미 닫힌 이슈:**
건너뛰고 로그에 기록: `#N 이미 닫혀 있어 건너뜁니다.`

**연결된 PR이 있는 경우:**
댓글에 명시: "관련 PR #X 가 이미 생성되어 있습니다."

---

## 옵션 요약

| 플래그 | 동작 |
|--------|------|
| `--dry-run` | 댓글 내용만 출력, 실제 게시 안 함 |
| `--issues N [N...]` | 지정한 이슈 번호만 처리 |
| `--state open\|closed\|all` | 가져올 이슈 상태 (기본값: open) |
| `--no-close` | 댓글만 달고 이슈는 닫지 않음 |

---

## 보안 주의사항

GitHub 토큰은 저장소 쓰기 권한을 가진다. API 호출 전에 반드시 `owner/repo`를 사용자에게 확인한다. 특히 이슈를 닫기 전에 한 번 더 확인한다. 토큰을 버전 관리에 커밋하지 않는다.
