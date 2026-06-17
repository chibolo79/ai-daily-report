---
name: image-organizer
description: "프로젝트 루트에 저장된 이미지를 자동 분류·정리하는 스킬. 명함이면 인물별 크롭 → 파일명 변경 → business_cards/ 이동 → 분석 파일 담당자 정보 업데이트까지 자동 처리. 명함 외 이미지는 방문일 기준 images/YYYY-MM-DD/ 폴더로 이동. '이미지 정리', '명함 정리', '사진 정리', '이미지 올렸어', '명함 저장했어' 등의 표현에 트리거."
status: "v1.0"
---

## 이 스킬이 하는 일

프로젝트 루트(`C:\Project.Claude\ai-daily-report\`)에 저장된 이미지를 자동 감지·분류·정리한다.

**명함 이미지** → 크롭 → 파일명 변경 → `images/business_cards/` → 분석 파일 업데이트  
**현장 사진 등** → `images/YYYY-MM-DD/` 폴더로 이동 + 적절한 파일명 변경

---

## 진행 순서

### Step 1: 루트 이미지 탐지

```powershell
Get-ChildItem "C:\Project.Claude\ai-daily-report" -MaxDepth 1 -Include "*.jpg","*.jpeg","*.png","*.heic","*.webp" | Sort-Object LastWriteTime -Descending
```

→ 루트에 이미지가 없으면 "정리할 이미지가 없습니다." 한 줄로 종료.

### Step 2: 이미지 Read → 내용 파악

각 이미지를 Read 도구로 읽어 내용 파악:
- **명함**인지 / **현장 사진·문서**인지 판별
- 명함이면: 1장인지 / 여러 장이 한 사진에 있는지 확인
- 각 명함에서 추출: 이름, 직함, 회사명, 연락처, 이메일

### Step 3: 명함 처리

#### 단일 명함 (1장)
1. 파일명 규칙에 맞게 이름 변경: `YYYYMMDD_회사명_영문이름.jpg`
2. `images/business_cards/`로 이동
3. 분석 파일 해당 업체 섹션 담당자 테이블에 추가

#### 복수 명함 (한 사진에 여러 장)
1. Python Pillow로 명함 수에 맞게 크롭
   - 2장: 좌/우 or 상/하 분할
   - 4장: 2×2 분할
   - 불규칙 배치: 시각적 경계 기준으로 개별 크롭
2. 각 명함을 개별 파일로 저장 후 위 단일 명함 절차 반복
3. 원본 파일 삭제

```python
from PIL import Image
img = Image.open(원본경로)
w, h = img.size
# 4분할 예시
regions = {
    '이름1': (0, 0, w//2, h//2),
    '이름2': (w//2, 0, w, h//2),
    '이름3': (0, h//2, w//2, h),
    '이름4': (w//2, h//2, w, h),
}
```

### Step 4: 현장 사진·문서 처리

1. 이미지 내용 파악: 어떤 업체 관련인지, 무엇을 찍은 것인지
2. 파일명 규칙: `업체명_내용설명.jpg` (예: `camex_sus304_spec.jpg`)
3. 방문일 기준 폴더 `images/YYYY-MM-DD/`로 이동
   - 방문일 불명확 시 사용자에게 확인

### Step 5: 분석 파일 업데이트

**명함인 경우** — 해당 업체 섹션 담당자 테이블에 반영:

```
Grep("### 업체명", 분석파일) → 라인 번호 확인
Read(해당 구간) → 담당자 테이블 위치 확인
Edit → 새 담당자 행 추가
```

추가 형식:
```
| **담당자 (YYYY 현재)** | **이름** (직함) — Tel: ... / Mobile: ... / 이메일 |
```

- 이미 동일 인물이 기재된 경우: 정보 업데이트만
- 해당 업체 섹션이 없는 경우: 채팅에 알림 후 사용자 확인

### Step 6: 최종 업데이트 타임스탬프 갱신

분석 파일 헤더 `**최종 업데이트**` 갱신.

---

## 파일명 규칙

| 유형 | 규칙 | 예시 |
|------|------|------|
| 명함 | `YYYYMMDD_회사명_영문이름소문자.jpg` | `20260617_advanex_nagumo_kazuhiro.jpg` |
| 현장 사진 | `업체명_내용설명.jpg` | `advanex_factory_overview.jpg` |
| 스펙시트 | `업체명_품목_spec.jpg` | `camex_sus304_spec.jpg` |

---

## 폴더 구조

```
images/
├── business_cards/     ← 모든 명함
└── YYYY-MM-DD/         ← 방문일별 현장 사진·문서
```

---

## Pillow 미설치 시

```powershell
pip install Pillow -q
```

자동 설치 후 진행. 실패 시 사용자에게 알림.

---

## 처리 완료 후 출력 형식

```
## 이미지 정리 완료

| 파일 | 유형 | 처리 결과 |
|------|------|----------|
| KakaoTalk_xxx.jpg | 명함 4장 | advanex_nagumo.jpg 등 4개로 분리 저장 |
| KakaoTalk_yyy.jpg | 명함 1장 | oristar_nguyen_thanh_huyen.jpg |

분석 파일 업데이트: ADVANEX 담당자 4명 추가
```

**전체 파일 Read 금지 (분석 파일). Grep → 부분 Read → Edit.**  
**편집 내용 채팅 재출력 금지. 완료 시 위 형식으로 한 번만 출력.**

---

## 성공 기준

- [ ] 루트 이미지 전부 정리됨 (루트에 이미지 0개)
- [ ] 명함: business_cards/ 에 인물별 파일로 저장
- [ ] 현장 사진: images/YYYY-MM-DD/ 에 저장
- [ ] 분석 파일 담당자 정보 업데이트 완료
- [ ] 최종 업데이트 타임스탬프 갱신
