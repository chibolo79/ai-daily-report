---
name: image-organizer
description: "프로젝트 루트에 저장된 이미지를 자동 분류·정리하는 스킬. 명함이면 인물별 크롭 → 파일명 변경 → business_cards/ 이동 → 분석 파일 담당자 정보 업데이트까지 자동 처리. 명함 외 이미지는 방문일 기준 images/YYYY-MM-DD/ 폴더로 이동. '이미지 정리', '명함 정리', '사진 정리', '이미지 올렸어', '명함 저장했어' 등의 표현에 트리거."
status: "v1.2"
---

## ⚠️ 필수 주의사항 (2026-06-17 사고 교훈)

### 1. 원본 파일 절대 훼손 금지
- **원본(`images/KakaoTalk_*.jpg` 등)은 절대 덮어쓰지 않는다**
- 크롭 작업은 반드시 `images/_staging/` 폴더에서 진행
- QA 합격 후에만 `images/business_cards/`로 복사
- `business_cards/` 안의 파일은 원본이 아님 — 재처리 시 원본 사진을 찾을 것

### 2. 크롭 도구 우선순위
Claude Code는 이미지 시각적 편집에 취약하다. 아래 순서로 도구를 선택한다:

| 우선순위 | 도구 | 방법 |
|---------|------|------|
| 1순위 | **remove.bg API** | 배경 자동 제거 + 카드 분리 |
| 2순위 | **Windows 사진 앱** | computer-use로 열어서 드래그 크롭 |
| 3순위 | **Python PIL + 비전 좌표** | 마지막 수단 — 반복 시도 최대 2회 |

### 3. 원본 확인 먼저
작업 시작 전 반드시:
```powershell
Get-ChildItem "C:\Project.Claude\ai-daily-report\images" -Filter "KakaoTalk_*.jpg"
```
원본 없으면 사용자에게 경로 확인 요청. 절대 이미 처리된 파일로 재시작하지 말 것.

---

## 이 스킬이 하는 일

프로젝트 루트(`C:\Project.Claude\ai-daily-report\`)에 저장된 이미지를 자동 감지·분류·정리한다.

**명함 이미지** → 크롭(외부툴 우선) → 파일명 변경 → `images/business_cards/` → 분석 파일 업데이트  
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

**반드시 2단계로 처리한다: ① 대략 분할 → ② 각 조각에서 명함만 정밀 크롭**

단순 50/50 분할만 하면 배경·인접 명함이 포함됨. 반드시 아래 정밀 크롭 함수를 적용.

```python
import cv2, numpy as np
from PIL import Image
import os

# Step 1: 균등 분할 (4장 예시)
img = Image.open(원본경로)
w, h = img.size
rough = {
    '이름1': img.crop((0, 0, w//2, h//2)),
    '이름2': img.crop((w//2, 0, w, h//2)),
    '이름3': img.crop((0, h//2, w//2, h)),
    '이름4': img.crop((w//2, h//2, w, h)),
}
for name, piece in rough.items():
    piece.save(f'tmp_{name}.jpg')

# Step 2: 각 조각에서 명함만 정밀 크롭
def crop_card_clean(img_path, out_path):
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    # 가장자리 8% 제외 (인접 명함·배경 노이즈 제거)
    mx, my = int(w * 0.08), int(h * 0.08)
    roi = img[my:h-my, mx:w-mx]

    # HSV 흰색/밝은 영역(명함 본체) 마스크
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 0, 170), (180, 50, 255))
    kernel = np.ones((15,15), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((8,8), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        # 폴백: 가장자리만 제거
        cv2.imwrite(out_path, roi, [cv2.IMWRITE_JPEG_QUALITY, 95])
        return

    c = max(contours, key=cv2.contourArea)
    x, y, bw, bh = cv2.boundingRect(c)
    pad = 8
    x1 = max(0, x + mx - pad)
    y1 = max(0, y + my - pad)
    x2 = min(w, x + mx + bw + pad)
    y2 = min(h, y + my + bh + pad)
    cv2.imwrite(out_path, img[y1:y2, x1:x2], [cv2.IMWRITE_JPEG_QUALITY, 95])
```

**주의**: 스티커·라벨 등 이물질이 명함 가장자리에 있으면 추가로 해당 방향 margin을 높여서 재크롭.

원본 파일은 처리 완료 후 삭제.

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
