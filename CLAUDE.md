# CLAUDE.md

프로젝트 개요 → [README.md](README.md) | 미션·원칙 → [SOUL.md](SOUL.md)

## Skills

### `/ai-agent-research-report`
**트리거**: "AI 리포트", "논문 추천", "2026 AI 트렌드", "인플루언서 맵", "기업 업데이트"  
**상세**: [SKILL.md](.claude/skills/ai-agent-research-report/SKILL.md)

### `/github-issue-resolver`
**트리거**: "이슈 해결", "이슈에 댓글 달고 닫아줘", GitHub 이슈 URL 붙여넣기  
**상세**: [SKILL.md](.claude/skills/github-issue-resolver/SKILL.md)

### `/briefing-improver`
**트리거**: "브리핑 개선", "전체 사이클", "약점 찾아서 고쳐줘", "이슈 만들고 해결하고 문서까지"  
**상세**: [SKILL.md](.claude/skills/briefing-improver/SKILL.md)

### `/doc-optimizer`
**트리거**: "문서 최적화", "세 문서 정리", "CLAUDE.md SOUL.md README.md 정리"  
**상세**: [SKILL.md](.claude/skills/doc-optimizer/SKILL.md)

## Operational Rules

**토큰**: 기본값은 `--web-search`. `--deep-research`는 사용자가 명시적으로 요청할 때만.

**Git**: 커밋·푸시·이슈 닫기는 사용자 확인 후 실행. 자동 실행하지 않는다.

**인코딩**: GitHub API에 한국어 전송 시 반드시 UTF-8 (`ensure_ascii=False`).

## Implementation Status

- `ai-agent-research-report`: 아키텍처·Git 통합 완성(80%). WebSearch 연동·GitHub Issues API 미구현
- `github-issue-resolver`: 완성, API 호출 검증됨

개선 과제 → [ISSUES.md](ISSUES.md)
