# Cerebellum Engine (소뇌 엔진)

**버전**: v0.6.0-beta  
**상태**: 산업 적용 가능

---

## 🎯 개요

소뇌 엔진은 **기억을 즉각 행동으로 변환하는 계층**입니다.

해마(Hippocampus)의 기억을 활용하여 즉각적인 보정 신호를 생성하는 독립적인 제어 모듈입니다.

---

## 🏭 적용 가능한 산업 분야

1. **정밀 가공** (우선순위 1)
   - 5축 CNC 머신
   - 마이크로 가공 (0.00001mm)
   - 다이아몬드 절삭

2. **로봇 팔 제어** (우선순위 2)
   - 산업용 로봇 팔
   - 수술 로봇
   - 픽 앤 플레이스

3. **항공기 제어** (우선순위 3)
   - 자동 조종 시스템
   - 공기역학적 지연 보정

4. 자율주행 차량, 의료 기기, 반도체 제조

---

## 🚀 빠른 시작

### 설치

```bash
cd package
pip install numpy
```

### 기본 사용

```python
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig
import numpy as np

# 소뇌 엔진 생성
config = CerebellumConfig()
engine = CerebellumEngine(memory_dim=5, config=config)

# 보정값 계산
correction = engine.compute_correction(
    current_state=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    target_state=np.array([1.0, 1.0, 0.0, 0.0, 0.0]),
    dt=0.001
)
```

### PID 제어기와 통합

```python
# PID 제어
pid_output = pid_controller.compute(error)

# 소뇌 보정
cerebellum_correction = cerebellum.compute_correction(...)

# 최종 제어 신호
final_control = pid_output + cerebellum_correction
```

---

## 📐 핵심 기능

### 1. Predictive Feedforward (예측 피드포워드)
다음 순간의 오차를 미리 예측하여 사전 보정

### 2. Trial-to-Trial 보정 (회차 학습)
반복 궤적에서 항상 생기던 오차를 기억하고 다음 시행에서 제거

### 3. Variance 감소 (떨림 필터링)
고주파 노이즈(떨림) 제거, 저주파 의도적 움직임 유지

### 4. 기억 기반 적응 (해마 연동)
해마의 기억을 즉각 행동으로 변환

---

## 📚 문서

- `FORMULA_REFERENCE.md`: 수식 참조 가이드
- `INDUSTRIAL_APPLICATIONS.md`: 산업 적용 분야
- `MODULE_INTEGRATION_GUIDE.md`: 통합 가이드
- `EXPERT_REVIEW.md`: 전문가 리뷰
- `WORK_LOG.md`: 작업 로그

---

## 🧪 테스트

```bash
# 전체 테스트 실행
python3 run_all_tests.py

# 개별 테스트
python3 test_cerebellum_standalone.py
python3 test_v0.6_features.py
```

---

## 📝 예시

```bash
# 정밀 가공 예시
python3 examples/precision_machining_example.py

# 로봇 팔 제어 예시
python3 examples/robot_arm_example.py

# 항공기 제어 예시
python3 examples/aircraft_control_example.py

# 호버링 학습
python3 scenarios/hovering_learning.py
```

---

## 📦 모듈화 원칙

- ✅ 독립적인 모듈로 완성
- ✅ 전체 엔진(쿠키 브레인) 완성 전에도 사용 가능
- ✅ 플러그 앤 플레이 방식
- ✅ 최소 의존성 (NumPy만 필요)

---

## 📄 라이선스

MIT License

---

## 👤 Author

GNJz

---

**버전**: v0.6.0-beta  
**업데이트**: 2026-01-22
