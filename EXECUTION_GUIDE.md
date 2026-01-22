# 소뇌 엔진 실행 가이드

## 📁 폴더 구조

```
5.Cerebellum_Engine/
├── README.md                          # 기본 설명
├── TEST_RESULTS.md                    # 테스트 결과
├── EXECUTION_GUIDE.md                 # 이 파일
└── package/
    ├── README.md                      # 패키지 설명
    ├── CEREBELLUM_DESIGN.md           # 설계 문서
    ├── CEREBELLUM_RESULTS.md          # 성능 지표 문서
    ├── cerebellum_demo.py             # 데모 (grid_engine 의존)
    ├── test_cerebellum_standalone.py  # 독립 테스트 ✅
    ├── cerebellum/
    │   ├── __init__.py
    │   └── cerebellum_engine.py       # 핵심 엔진 (373줄)
    └── benchmarks/
        └── benchmark_hippo_vs_hippo_cb.py
```

## 🚀 실행 방법

### 1. 독립 테스트 (권장)

**의존성 없이 소뇌 엔진만 테스트**

```bash
cd /Users/jazzin/Desktop/00_BRAIN/5.Cerebellum_Engine/package
python3 test_cerebellum_standalone.py
```

**테스트 항목**:
- ✅ 기본 초기화
- ✅ Predictive Feedforward
- ✅ Variance 감소
- ✅ 해마 메모리 통합
- ✅ Trial-to-Trial 보정

### 2. 데모 실행

**해마-소뇌 통합 데모** (grid_engine 의존성 필요)

```bash
cd /Users/jazzin/Desktop/00_BRAIN/5.Cerebellum_Engine/package
python3 cerebellum_demo.py
```

**주의**: `grid_engine` 모듈이 필요합니다.

### 3. 벤치마크 실행

**해마만 vs 해마+소뇌 성능 비교** (grid_engine 의존성 필요)

```bash
cd /Users/jazzin/Desktop/00_BRAIN/5.Cerebellum_Engine/package
python3 benchmarks/benchmark_hippo_vs_hippo_cb.py
```

## 📊 테스트 결과

### 독립 테스트 결과 (2026-01-22)

```
✅ 모든 테스트 통과!

테스트 1: 기본 초기화 ✅
테스트 2: Predictive Feedforward ✅
테스트 3: Variance 감소 ✅
테스트 4: 해마 메모리 통합 ✅
테스트 5: Trial-to-Trial 보정 ✅
```

## 🔧 사용 예시

### 기본 사용

```python
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig
import numpy as np

# 소뇌 엔진 생성
config = CerebellumConfig()
engine = CerebellumEngine(memory_dim=5, config=config)

# 보정값 계산
current_state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
target_state = np.array([1.0, 1.0, 0.0, 0.0, 0.0])
velocity = np.array([0.1, 0.1, 0.0, 0.0, 0.0])
acceleration = np.array([0.01, 0.01, 0.0, 0.0, 0.0])

correction = engine.compute_correction(
    current_state=current_state,
    target_state=target_state,
    velocity=velocity,
    acceleration=acceleration,
    dt=0.001
)

print(f"Correction: {correction}")
```

### 해마 메모리 통합

```python
from cerebellum.cerebellum_engine import CerebellumEngine
import numpy as np

# 해마 메모리 (모의 객체)
class MockMemory:
    def retrieve(self, key, context=None):
        # 기억 검색 로직
        return [{'bias': np.array([0.001, 0.002, 0.0, 0.0, 0.0]), 'confidence': 0.9}]

memory = MockMemory()

# 소뇌 엔진 생성 (메모리 연결)
engine = CerebellumEngine(memory_dim=5, memory=memory)

# 보정값 계산 (메모리 활용)
correction = engine.compute_correction(
    current_state=current_state,
    target_state=target_state,
    context={"tool": "tool_A"},
    dt=0.001
)
```

## ⚠️ 주의사항

1. **독립 테스트**: `test_cerebellum_standalone.py`는 의존성 없이 실행 가능
2. **데모/벤치마크**: `grid_engine` 모듈이 필요 (별도 설치 필요)
3. **메모리 통합**: 해마 메모리는 선택적 (None 가능)

## 📝 파일 크기

- `cerebellum_engine.py`: 373줄
- `test_cerebellum_standalone.py`: ~250줄
- `cerebellum_demo.py`: 204줄
- `benchmark_hippo_vs_hippo_cb.py`: ~324줄

## ✅ 상태

- **구현**: 완료 ✅
- **테스트**: 통과 ✅
- **독립 실행**: 가능 ✅
- **문서화**: 완료 ✅

