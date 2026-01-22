# Cerebellum Engine (소뇌 엔진)

**버전**: v0.6.0-beta  
**상태**: 산업 적용 가능  
**라이선스**: MIT License

---

## 📖 소뇌(Cerebellum)란?

소뇌는 뇌의 후두엽 아래에 위치한 기관으로, **기억을 즉각 행동으로 변환하는 계층**입니다.

### 생물학적 역할

1. **운동 제어**: 정확한 움직임 조절
2. **예측 제어**: 다음 순간의 오차를 미리 예측하여 보정
3. **학습**: 반복되는 동작에서 패턴을 학습하고 개선
4. **떨림 억제**: 미세한 진동을 필터링하여 안정적인 움직임 유지

### 해마와의 관계

- **해마(Hippocampus)**: "무엇을 기억할지" 결정
- **소뇌(Cerebellum)**: "기억을 즉시 행동으로 변환"

해마가 저장한 기억을 소뇌가 즉각적인 제어 신호로 변환하여 정확한 동작을 수행합니다.

---

## 🎯 Cerebellum Engine의 핵심 기능

### 1. Predictive Feedforward (예측 피드포워드)

**수식**: `e_pred(t+Δt) = e(t) + v(t)·Δt + ½a(t)·(Δt)²`

다음 순간의 오차를 미리 예측하여 사전에 보정합니다. 물리적 시스템의 지연 시간을 고려하여 오차가 발생하기 전에 미리 대응합니다.

**적용 예시**:
- 로봇 팔이 목표 지점에 도달하기 전에 궤적을 미리 보정
- 항공기가 자세를 변경할 때 공기역학적 지연을 고려한 예측 제어

### 2. Trial-to-Trial 보정 (회차 학습)

**수식**: `trial_error = e(t) - b_hip(x(t), c(t))`

반복되는 궤적에서 항상 생기던 오차를 해마에 기억하고, 다음 시행에서 미리 제거합니다. 인간이 악기나 운동을 배울 때와 동일한 방식입니다.

**적용 예시**:
- CNC 가공에서 반복 작업 시 발생하는 미세한 편차 제거
- 로봇 팔의 반복 동작에서 정확도 향상

### 3. Variance 감소 (떨림 필터링)

**수식**: `high_freq_noise = e(t) - filtered_error`

고주파 노이즈(떨림)를 제거하면서 저주파 의도적 움직임은 유지합니다. 소뇌의 Tremor Suppression 기능을 구현합니다.

**적용 예시**:
- 수술 로봇의 미세한 떨림 제거
- 정밀 가공에서 진동 필터링

### 4. 기억 기반 적응 (해마 연동)

**수식**: `memory_correction = -b_hip(x(t), c(t)) · α_memory · confidence · context_weight`

해마의 기억을 즉각 행동으로 변환합니다. 같은 위치라도 상황(context)에 따라 다른 보정을 적용할 수 있습니다.

**적용 예시**:
- 특정 온도에서 발생하는 오차를 기억하고 자동 보정
- 도구나 환경에 따른 적응형 제어

---

## 🏭 산업 적용 분야

### 1. 정밀 가공 (우선순위 1)
- **5축 CNC 머신**: 0.00001mm 단위의 초정밀 가공
- **마이크로 가공**: 반도체 제조, 의료 기기
- **다이아몬드 절삭**: 극한 정밀도 요구 작업

### 2. 로봇 팔 제어 (우선순위 2)
- **산업용 로봇 팔**: 픽 앤 플레이스, 용접, 조립
- **수술 로봇**: 미세한 떨림 제거, 정확한 궤적 추적
- **서비스 로봇**: 부드러운 동작, 안정적인 제어

### 3. 항공기 제어 (우선순위 3)
- **자동 조종 시스템**: 공기역학적 지연 보정
- **드론 제어**: 안정적인 호버링, 정확한 궤적 추적
- **항공기 자세 제어**: 부드러운 기동

### 4. 기타 분야
- 자율주행 차량: 정확한 조향 제어
- 의료 기기: 정밀한 위치 제어
- 반도체 제조: 극한 정밀도 요구 작업

---

## 🚀 빠른 시작

### 설치

```bash
pip install numpy
```

### 기본 사용

```python
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig
import numpy as np

# 소뇌 엔진 생성
config = CerebellumConfig(
    feedforward_gain=0.5,
    trial_gain=0.3,
    variance_gain=0.2,
    memory_gain=0.4
)
engine = CerebellumEngine(memory_dim=5, config=config)

# 보정값 계산
correction = engine.compute_correction(
    current_state=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    target_state=np.array([1.0, 1.0, 0.0, 0.0, 0.0]),
    velocity=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    acceleration=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    dt=0.001
)
```

### PID 제어기와 통합

```python
# PID 제어 (기본 제어)
pid_output = pid_controller.compute(error)

# 소뇌 보정 (정밀 보정)
cerebellum_correction = cerebellum.compute_correction(
    current_state=current_state,
    target_state=target_state,
    velocity=velocity,
    acceleration=acceleration,
    context={'mode': 'precision_control'},
    dt=0.001
)

# 최종 제어 신호 (PID + Cerebellum)
final_control = pid_output + cerebellum_correction
```

---

## 📚 문서

- `FORMULA_REFERENCE.md`: 수식 참조 가이드
- `INDUSTRIAL_APPLICATIONS.md`: 산업 적용 분야 상세
- `MODULE_INTEGRATION_GUIDE.md`: 통합 가이드
- `EXPERT_REVIEW.md`: 전문가 리뷰
- `WORK_LOG.md`: 작업 로그

---

## 🧪 테스트

```bash
cd package
python3 run_all_tests.py
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

- ✅ **독립적인 모듈**: 전체 엔진(쿠키 브레인) 완성 전에도 사용 가능
- ✅ **플러그 앤 플레이**: 기존 제어 시스템에 쉽게 통합
- ✅ **최소 의존성**: NumPy만 필요
- ✅ **산업 적용 가능**: 실제 기계에 바로 적용 가능

---

## 🔬 버전 정보

### v0.6.0-beta (현재 버전)

**신규 기능**:
- Confidence 기반 gain 조절: 기억의 신뢰도에 따른 적응형 보정
- Error norm 기반 saturation: 과도한 보정 신호 방지
- Context 가중치: 상황에 따른 적응형 반응

**핵심 기능**:
- Predictive Feedforward
- Trial-to-Trial 보정
- Variance 감소
- 기억 기반 적응

---

## 👤 Author

GNJz

---

## 📄 License

MIT License

---

**버전**: v0.6.0-beta  
**업데이트**: 2026-01-22
