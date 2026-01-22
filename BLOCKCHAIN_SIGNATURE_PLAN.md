# 소뇌 엔진 블록체인 서명 계획

**작성일**: 2026-01-22

---

## 🔍 현재 상태 확인

### ✅ Git 해시 기록
- 커밋 해시: 9개 커밋
- 최신 해시: `cbbac55b5bbd533e20094125f4567f6117e60bdc`
- 수정 이력: 완전히 기록됨

### ❌ 블록체인 서명
- PHAM 블록체인 서명: 없음
- 해시 기록 파일: 없음
- PHAM 연동: 안 됨

---

## 📋 블록체인 서명 프로세스

### PHAM Sign v4 시스템

**위치**: `cookiie_brain/blockchain/pham_sign_v4.py`

**기능**:
1. 파일 해시 생성 (SHA-256)
2. 블록체인 서명 생성
3. 수정 사항 추적 (4-Signal Scoring)
4. IPFS 업로드 (선택)
5. 수익 분배 기록

**4-Signal Scoring**:
- Byte (25%): 바이트 변경량
- Text (35%): 텍스트 유사도 변화
- AST (30%): 코드 구조 변경
- Exec (10%): 실행 결과 변화

---

## 🎯 소뇌 엔진 서명 계획

### 1단계: 핵심 파일 서명

**서명 대상 파일**:
1. `package/cerebellum/cerebellum_engine.py` (핵심 엔진)
2. `package/cerebellum/__init__.py`
3. `README.md` (한국어)
4. `README_EN.md` (영어)

**명령어**:
```bash
cd /Users/jazzin/Desktop/00_BRAIN/cookiie_brain/blockchain

# 핵심 엔진 서명
python3 pham_sign_v4.py ../../5.Cerebellum_Engine/package/cerebellum/cerebellum_engine.py \
    --author "GNJz" \
    --desc "Cerebellum Engine v0.6.0-beta - 산업용 제어 시스템"

# README 서명
python3 pham_sign_v4.py ../../5.Cerebellum_Engine/README.md \
    --author "GNJz" \
    --desc "Cerebellum Engine README (Korean)"
```

### 2단계: 블록체인 체인 파일 생성

**생성될 파일**:
- `blockchain/pham_chain_cerebellum_engine.json`
- `blockchain/pham_chain_cerebellum_readme.json`

**내용**:
- 각 수정마다 블록 추가
- 해시 체인으로 연결
- 수정 사항 추적

### 3단계: 수정 사항 추적

**자동 추적**:
- 파일 수정 시 해시 변경 감지
- 4-Signal Scoring으로 기여도 계산
- 블록체인에 새 블록 추가

---

## 📊 서명 후 예상 구조

```
5.Cerebellum_Engine/
├── package/
│   └── cerebellum/
│       └── cerebellum_engine.py (서명됨)
├── README.md (서명됨)
├── README_EN.md (서명됨)
└── blockchain/ (생성 예정)
    ├── pham_chain_cerebellum_engine.json
    ├── pham_chain_readme.json
    └── pham_sign_v4.py (복사 또는 링크)
```

---

## 🔧 실행 계획

### 즉시 실행

1. PHAM 서명 도구 확인
2. 핵심 파일 서명
3. 블록체인 체인 파일 생성
4. 수정 이력 기록

---

**다음 단계**: PHAM 서명 실행

