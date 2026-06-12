#!/bin/bash

TOKEN="${GITHUB_TOKEN}"
OWNER="chibolo79"
REPO="ai-daily-report"
API_URL="https://api.github.com/repos/$OWNER/$REPO/issues"

# 이슈 1: 토큰 낭비
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #1: 토큰 낭비" || echo "❌ #1: 실패"
{
  "title": "토큰 낭비: deep-research 워크플로우 비효율",
  "body": "## 문제\n\n- deep-research 워크플로우 사용으로 **1,963,813 토큰** 소비\n- 5방향 병렬 검색 + 15개 소스 수집 + 3-vote 교차 검증 = 오버킬\n\n## 영향\n\n- 일회성 리서치는 괜찮지만, 매일 자동화하면 월 **60M 토큰** 필요\n- 지속 불가능한 토큰 비용\n\n## 해결책\n\n- 단순 **WebSearch**로 충분 (토큰 50K~100K)\n- **토큰 20배 절감** 가능",
  "labels": ["optimization", "research", "high-priority"]
}
EOF

# 이슈 2: 논문 추천
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #2: 논문 추천" || echo "❌ #2: 실패"
{
  "title": "논문 추천 신뢰성 부족 - GLEAN 1편만 추천",
  "body": "## 문제\n\n- \"2026년 딱 한편의 논문\"이라는 요청에 응해 GLEAN만 선택\n- deep-research 결과에서 다른 유망 논문들도 3-0 vote로 동등 평가:\n  - **LightMem** (메모리 관리 혁신, ICLR 2026)\n  - **OpenHands** (실무 구현 가능, ICLR 2025, 188 contributors)\n  - **MAST** (멀티에이전트 실패 분석, NeurIPS 2025 Spotlight)\n  - **CORAL** (진화 기반 자동 발견)\n\n## 영향\n\n- GLEAN 선택 이유가 주관적\n- 독자가 \"왜 GLEAN인가\"를 납득하기 어려움\n\n## 해결책\n\n- **TOP 5 논문** 형식으로 변경\n- 각 논문의 강점을 비교 설명",
  "labels": ["content", "research", "medium-priority"]
}
EOF

# 이슈 3: 인플루언서
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #3: 인플루언서" || echo "❌ #3: 실패"
{
  "title": "인플루언서 활동 상태 미확인",
  "body": "## 문제\n\n- 지식 컷오프: 2025년 8월\n- 현재 시점: 2026년 6월 (**10개월 차이**)\n- 추천 인플루언서의 현재 활동 상태 미확인\n\n## 영향\n\n- 비활동 인플루언서를 추천할 가능성\n- 새로운 주요 인물 발굴 미실시\n\n## 해결책\n\n- 웹 검색으로 **현재 활동** 상태 확인\n- 최근 3개월 콘텐츠 확인\n- 필요시 인플루언서 교체",
  "labels": ["content", "outdated", "medium-priority"]
}
EOF

# 이슈 4: 기업 업데이트
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #4: 기업 업데이트" || echo "❌ #4: 실패"
{
  "title": "기업 업데이트 정보 불완전",
  "body": "## 문제\n\n- 기업 업데이트는 학습 데이터(2025년 8월)만으로 작성\n- 웹 검색 없이 진행됨\n- 2025년 하반기~2026년 6월 정보 누락 가능\n\n## 영향\n\n- \"2026년 6월 기준\" 리포트인데 실제로는 2025년 8월 수준\n- 최신 트렌드 놓칠 가능\n\n## 해결책\n\n- 웹 검색으로 **2025년 9월~2026년 6월** 업데이트 추가 조사\n- 공식 블로그 확인 (anthropic.com, openai.com, blog.google)\n- 리포트 갱신",
  "labels": ["content", "outdated", "medium-priority"]
}
EOF

# 이슈 5: 리포트 구조
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #5: 리포트 구조" || echo "❌ #5: 실패"
{
  "title": "리포트 구조 불균형 - GLEAN만 깊이 있게 설명",
  "body": "## 문제\n\n- GLEAN: 문제 정의, 해결책, 실험 결과, 실무 활용법 **상세 설명**\n- 다른 논문들: 1-2줄 언급만\n- 인플루언서: 선정 이유 상세하지만 다른 콘텐츠 부족\n\n## 영향\n\n- 독자가 GLEAN에 편향된 이해\n- 다른 논문/커뮤니티에 대한 이해도 낮음\n\n## 해결책\n\n- TOP 5 논문 각각에 **동등한 깊이** 제공\n- 비교 분석 섹션 추가\n- 사용 사례별 추천 테이블",
  "labels": ["content", "structure", "low-priority"]
}
EOF

# 이슈 6: 자동화 계획
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #6: 자동화 계획" || echo "❌ #6: 실패"
{
  "title": "자동화 계획 미성숙 - 매일 생성은 비현실적",
  "body": "## 문제\n\n- 초기 계획: \"매일 08:00에 리포트 자동 생성\"\n- 현실: deep-research로 매일 2M 토큰 소비 → 월 60M\n- 같은 정보를 매일 다시 검색하는 비효율\n\n## 영향\n\n- 토큰 비용 폭탄\n- 필요 없는 정보 중복\n\n## 해결책\n\n- **주 1회** (월요일) 깊이 있는 리서치\n- **일 1회** (08:00) 뉴스 헤드라인 요약만\n- **월 1회** (말일) 완전한 리포트 업데이트",
  "labels": ["automation", "planning", "high-priority"]
}
EOF

# 이슈 7: YouTube
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #7: YouTube" || echo "❌ #7: 실패"
{
  "title": "YouTube 채널 제외 검토",
  "body": "## 문제\n\n- 초기 요청에 YouTube가 없어서 제외함\n- 하지만 AI 에이전트 분야 주요 YouTube 채널:\n  - **Yannic Kilcher** (논문 해설)\n  - **Two Minute Papers** (연구 요약)\n  - **AI Explained** (트렌드 분석)\n\n## 영향\n\n- 유명 채널을 추천하지 못함\n- 인플루언서 맵이 불완전\n\n## 해결책\n\n- 사용자 요청 확인 후 YouTube 채널 추가 여부 결정\n- 필요시 Reddit + X + YouTube 균형 맞추기",
  "labels": ["content", "research", "low-priority"]
}
EOF

# 이슈 8: 출처 검증
curl -s -X POST "$API_URL" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF' > /dev/null && echo "✅ #8: 출처 검증" || echo "❌ #8: 실패"
{
  "title": "출처 인용 검증 미부족",
  "body": "## 문제\n\n- 링크는 많지만 모두 검증된 최신 정보인지 불명확\n- 일부 아카이브 링크 또는 변경된 링크 가능\n- 2025년 8월 이후 링크는 깨질 수 있음\n\n## 영향\n\n- 독자가 링크 따라갔을 때 404 에러 가능\n- 신뢰도 저하\n\n## 해결책\n\n- 월 1회 링크 유효성 점검 (linkchecker 도구)\n- 깨진 링크 수정\n- 최신 공식 링크로 교체",
  "labels": ["quality", "verification", "low-priority"]
}
EOF

echo ""
echo "✅ 모든 이슈가 제대로 생성되었습니다!"
