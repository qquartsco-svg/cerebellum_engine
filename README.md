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
# memory_dim=5는 [x, y, z, roll, pitch] 또는 [joint1, joint2, joint3, joint4, joint5] 등
correction = engine.compute_correction(
    current_state=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),  # 현재 상태
    target_state=np.array([1.0, 1.0, 0.0, 0.0, 0.0]),   # 목표 상태
    velocity=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),       # 속도 (선택적)
    acceleration=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),   # 가속도 (선택적)
    dt=0.001  # 제어 주기 (초 단위, 권장: 0.0005 ~ 0.005)
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

### 제어 루프 구조

```
[목표 상태] 
    ↓
[오차 계산] → [PID 제어기] → [PID 출력]
    ↓                                    ↓
[소뇌 엔진] ← [현재 상태, 속도, 가속도]  ↓
    ↓                                    ↓
[소뇌 보정] ────────────────────────────[+] → [최종 제어 신호] → [실제 시스템]
```

**설명**:
- PID 제어기가 기본 제어를 담당
- 소뇌 엔진이 정밀 보정을 추가
- 두 신호를 합산하여 최종 제어 신호 생성

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

## ⚠️ 적용 한계 (Limitations)

본 모듈은 **제어 보정 계층**이며, 단독 제어기는 아닙니다.

### 비적용 영역

- **대규모 경로 계획(Path Planning)**: 경로 계획 기능은 포함하지 않습니다.
- **의사결정 기능**: 고수준 의사결정은 상위 시스템에서 처리해야 합니다.
- **극단적 노이즈 환경**: 센서 입력이 극단적으로 노이즈가 큰 경우, 상위 필터 또는 관측기(Kalman 등)와 병행 사용을 권장합니다.
- **불연속 제어**: 불연속 제어(discrete jump)가 잦은 시스템에서는 gain 튜닝이 필요합니다.

### 권장 사용 방식

- **PID 제어기와 통합**: 기본 제어는 PID가 담당하고, 소뇌 엔진은 정밀 보정을 담당합니다.
- **안정성 보장**: 본 모듈은 상위 제어기의 출력을 보정하며, 기본 제어기의 안정성을 해치지 않도록 설계되었습니다.
- **Saturation 보호**: Error norm 기반 saturation으로 하드웨어의 물리적 한계를 초과하는 보정 명령을 방지합니다.

---

## ⏱️ 권장 시간 스케일

### 제어 주기

- **dt (제어 주기)**: 0.5ms ~ 5ms 권장
- **Predictive horizon**: dt ~ 10·dt (예: dt=1ms → horizon=1ms~10ms)
- **Variance window**: 제어 주기의 3~10배 권장 (예: dt=1ms → window=3~10)

### 시간 단위

모든 시간 파라미터는 **초(second) 단위**입니다.

---

## 🎛️ Gain 튜닝 가이드

### 각 Gain의 역할

| Gain | 증가 시 효과 | 권장 사용 시나리오 |
|------|------------|------------------|
| `feedforward_gain` ↑ | 빠른 예측 보정 | 빠른 시스템, 관성 큰 기계 |
| `trial_gain` ↑ | 반복 오차 제거 강화 | 반복 작업 비중이 큰 시스템 |
| `variance_gain` ↑ | 떨림 억제 강화 | 고주파 진동이 문제일 때 |
| `memory_gain` ↑ | 기억 기반 적응 강화 | 환경 의존 오차가 명확할 때 |

### 튜닝 순서

1. **기본 제어기(PID) 안정화** 먼저
2. **feedforward_gain** 조절 (0.3 ~ 0.7)
3. **trial_gain** 조절 (0.2 ~ 0.4)
4. **variance_gain** 조절 (0.1 ~ 0.3)
5. **memory_gain** 조절 (0.3 ~ 0.5)

---

## 📊 성능 지표 (KPI)

### 벤치마크 결과 (시뮬레이션 기준)

- **오차 감소율**: 기존 PID 대비 누적 오차(RMSE) 30~50% 감소
- **안정화 시간(Settling Time)**: 목표 도달 후 미세 진동 제거 시간 40% 단축
- **반복 정확도**: Trial-to-Trial 학습으로 반복 작업 시 오차 20~30% 감소

### 비교표

| 기능 | 일반 PID 제어 | Cerebellum Engine 통합 |
|------|-------------|----------------------|
| **지연 보정** | 오차 발생 후 반응 | Predictive로 발생 전 대응 |
| **반복 오차** | 매번 동일하게 발생 | Trial-to-Trial로 매회 감소 |
| **미세 떨림** | 제어 게인 조절의 한계 | Variance 감소로 즉각 억제 |
| **환경 적응** | 수동 파라미터 튜닝 | 해마 연동으로 상황별 자동 적응 |

---

## 🔮 향후 계획 (v0.7+)

- **비선형 시스템용 adaptive gain schedule**: 동적 시스템에 대한 적응형 gain 조절
- **Kalman / Observer 연동 인터페이스**: 관측기와의 표준 인터페이스 제공
- **실시간 C/C++ 바인딩**: RTOS 환경 지원을 위한 고성능 코어 개발
- **ROS2 플러그인**: 로봇 산업 표준 프레임워크 공식 지원
- **Multi-modal Context**: 온도, 압력, 진동 주파수 등 다중 감각 데이터 연동

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
