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

### `/vietnam-visit-report`
**트리거**: "베트남 보고서", "출장 보고서", "방문 보고서", "미팅 결과 정리", "vietnam report"  
**상세**: [SKILL.md](.claude/skills/vietnam-visit-report/SKILL.md)

### `vietnam-sales-updater` (서브에이전트)
**트리거**: "업체 정보 업데이트", "방문 이력 추가", "세일즈 현황 수정", "업체 섹션 추가", `회사명 / 항목 / 내용` 형식 입력  
**상세**: [vietnam-sales-updater.md](.claude/agents/vietnam-sales-updater.md)  
※ 슬래시 명령어가 아닌 자연어로 호출. 분석 파일 직접 편집 전담.

## Operational Rules

**토큰**: 기본값은 `--web-search`. `--deep-research`는 사용자가 명시적으로 요청할 때만.

**Git**: 커밋·푸시·이슈 닫기는 사용자 확인 후 실행. 자동 실행하지 않는다.

**인코딩**: GitHub API에 한국어 전송 시 반드시 UTF-8 (`ensure_ascii=False`).

**로컬 파일 참조**: 영업 보고서 작성 시 `C:\Work\` 하위 DOCX·XLSX·PDF를 직접 읽는다. pandoc 또는 Python xml 파싱 사용. 파일 경로는 사용자가 제공한다.

**Git Push 인증**: PAT(Personal Access Token)를 URL에 인라인으로 사용 (`https://user:token@github.com/...`). 토큰은 저장하지 않으며 사용 후 즉시 폐기를 안내한다.

## 파일 편집 효율 규칙 (토큰·시간 절약)

**Read 최소화**: 파일 전체를 Read하지 않는다.  
→ 순서: `Grep(회사명/섹션명)` → 라인 번호 확인 → `Read(offset, limit ±40줄)` → `Edit`

**Write 금지**: 기존 파일은 반드시 Edit 사용. Write(전체 재작성)는 신규 파일 생성 시에만.

**채팅 재출력 금지**: 편집 내용을 채팅에 표시하지 않는다. 완료 시 한 줄로 종료.

**사용자 입력 표준 형식**: 업체 정보·세일즈 현황 업데이트 시 아래 형식으로 받으면 파싱 없이 바로 Edit 실행.  
→ `회사명 / 변경 항목 / 새 내용`  
→ 예: `CAMEX / 담당자 / Mr. A (Director)`

## 베트남 분석 파일 업체 섹션 포맷 (필수)

분석 파일(`2026-06-14_Oristar_Vietnam_Sales_Analysis.md`)의 각 업체는 아래 구조를 유지한다. 요약 테이블로 묶지 않는다.

```
### [회사명]
| 항목 | 내용 |
|------|------|
| **담당자** | ... |
| **주소** | ... |
| **연락처** | ... |
| **이메일** | ... |
| **홈페이지** | ... |

**회사 개요**: ...
**세일즈 현황**: ...
**방문 이력**: ...
**영업 포인트**: ...
```

- 미확인 항목: `(미확인 — 방문 시 확인 필요)` 로 명시. 공란 불가.
- 주소 혼선 시: ※ 주석 병기 + "방문 시 Map Pin 확인 필요" 추가.
- 새 섹션 삽입: `---` 구분선을 Grep해서 위치 찾고 Edit.

## Implementation Status

- `ai-agent-research-report`: 아키텍처·Git 통합 완성(80%). WebSearch 연동·GitHub Issues API 미구현
- `github-issue-resolver`: 완성, API 호출 검증됨
- `vietnam-visit-report`: 스킬 정의 완성. 분석 문서(`2026-06-14_Oristar_Vietnam_Sales_Analysis.md`) 생성 및 누적 관리 중. 스크립트 자동화 미구현(수동 작성 방식)

개선 과제 → [ISSUES.md](ISSUES.md)
