---
name: briefing-improver
description: 프로젝트 약점 발굴→GitHub 이슈 등록→이슈 해결·종료→문서 최적화를 한 번에 순서대로 실행하는 스킬. "브리핑 개선", "briefing-improver", "프로젝트 한 번 쭉 정리해줘", "이슈 만들고 해결하고 문서까지", "전체 사이클 돌려줘", "약점 찾아서 고쳐줘" 등의 표현에 트리거. 세 절차(이슈 작성·이슈 처리·문서 최적화)를 한꺼번에 실행하고 싶을 때 반드시 사용.
status: "v1.0"
---

세 단계를 순서대로 실행한다. 각 단계가 완료된 뒤 다음으로 넘어간다.

---

## ⓐ issue-writer — 약점 발굴 → GitHub 이슈 등록

**목적**: 프로젝트의 현재 약점을 찾아 GitHub Issues로 등록한다.

### 절차

1. **약점 수집** — 아래 소스를 순서대로 읽는다:
   - `ISSUES.md` — 이미 파악된 개선 과제
   - 최신 리포트 파일 (`*_AI_Agent_Research_Report.md`) — 콘텐츠 품질 문제
   - `CLAUDE.md`의 Implementation Status — 미구현 기능

2. **이슈 분류** — 각 약점에 레이블을 붙인다:
   - 우선순위: `high` / `medium` / `low`
   - 카테고리: `skill` / `report` / `automation` / `docs`
   - 유형: `bug` / `enhancement` / `refactor`

3. **GitHub 이슈 등록** — GitHub API로 각 약점을 이슈로 생성한다.
   - 토큰: `$env:GITHUB_TOKEN` 또는 `$env:GH_TOKEN` 확인 → 없으면 사용자에게 요청
   - 저장소: `git remote get-url origin` 으로 `owner/repo` 파싱
   - 등록 전 목록을 사용자에게 보여주고 확인받는다

   ```python
   import json, urllib.request
   headers = {
       "Authorization": f"token {token}",
       "Content-Type": "application/json; charset=utf-8",
       "User-Agent": "claude-agent",
   }
   payload = json.dumps({
       "title": issue_title,
       "body": issue_body,
       "labels": labels,
   }, ensure_ascii=False).encode("utf-8")
   req = urllib.request.Request(
       f"https://api.github.com/repos/{repo}/issues",
       data=payload, method="POST", headers=headers
   )
   urllib.request.urlopen(req)
   ```

4. **완료 보고** — 등록된 이슈 번호·제목 목록 출력

---

## ⓑ issue-runner — 오픈 이슈 확인 → 작업 → 종료

**목적**: 등록된 오픈 이슈를 모두 처리하고 닫는다.

→ 상세 절차는 [`github-issue-resolver/SKILL.md`](.claude/skills/github-issue-resolver/SKILL.md) 참조.

**요약 흐름**:
1. `GET /repos/{owner}/{repo}/issues?state=open` 로 목록 조회
2. 각 이슈의 `title` + `body` + `labels` 읽어 해결 방안 댓글 작성
3. 댓글 POST → 이슈 PATCH `{"state": "closed"}`
4. 한국어 포함 시 반드시 UTF-8 (`ensure_ascii=False`)
5. 모든 이슈 처리 후 ✅/❌ 요약 출력

---

## ⓒ doc-optimizer — 문서 최적화

**목적**: CLAUDE.md·SOUL.md·README.md 세 파일의 역할 분리 원칙 준수 여부를 점검하고 정제한다.

→ 상세 절차는 [`doc-optimizer/SKILL.md`](.claude/skills/doc-optimizer/SKILL.md) 참조.

**요약 흐름**:
1. 세 파일 읽기
2. 중복 사실·위치 오류 탐지
3. 올바른 파일로 이동, 나머지는 링크 대체
4. 결과 요약 출력 (이동한 내용·라인 수 변화)

---

## 전체 실행 요약 출력

세 단계 완료 후 아래 형식으로 최종 보고한다:

```
## briefing-improver 완료

### ⓐ issue-writer
- 등록된 이슈: #N 제목, #N 제목 ...

### ⓑ issue-runner
- 처리 완료: ✅ #N, ✅ #N ...
- 실패: ❌ #N (사유)

### ⓒ doc-optimizer
- 이동한 내용: ...
- 라인 수 변화: SOUL.md N→M, README.md N→M, CLAUDE.md N→M
```

---

## 주의사항

- ⓐ 이슈 등록 전, ⓑ 이슈 닫기 전 — 각각 사용자 확인을 받는다. 자동 실행하지 않는다.
- GitHub 토큰을 로그에 출력하지 않는다.
- ⓐ에서 등록할 이슈가 없으면 ⓑ로 바로 넘어간다.
- ⓑ에서 오픈 이슈가 없으면 그 사실을 알리고 ⓒ로 넘어간다.
