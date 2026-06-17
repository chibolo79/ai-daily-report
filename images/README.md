# images/

미팅·출장 중 수집한 이미지 보관 폴더.

## 폴더 구조

```
images/
  YYYY-MM-DD/          ← 방문일 기준
    spec_*.jpg         ← 스펙시트
    whiteboard_*.jpg   ← 화이트보드 메모
    product_*.jpg      ← 제품 사진
    inquiry_*.jpg      ← Inquiry 관련 문서
  business_cards/      ← 명함 (보고서 미포함)
    YYYYMMDD_회사명_이름.jpg
```

## 규칙

- 보고서(MD/DOCX)에 포함할 이미지: `YYYY-MM-DD/` 하위에 저장
- 명함: `business_cards/`에 저장, 보고서에는 포함하지 않음
- 파일명은 내용을 알 수 있게 명시 (예: `camex_sus304_spec.jpg`)
- 보고서 삽입 시 마크다운: `![설명](../images/YYYY-MM-DD/파일명.jpg)`
- DOCX 최종 보고서 요청 시 해당 날짜 폴더 이미지 자동 포함
