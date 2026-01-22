# 소뇌 엔진 모듈 통합 가이드

**버전**: v0.6.0-beta  
**원칙**: 모듈화 & 핵심 부품화

---

## 🎯 핵심 원칙

**소뇌 엔진은 독립적인 모듈**
- 전체 엔진(쿠키 브레인) 완성 전에도 사용 가능
- 플러그 앤 플레이 방식
- 최소 의존성 (NumPy만 필요)

---

## 📦 모듈 구조

```
CerebellumEngine (독립 모듈)
├── Core: cerebellum_engine.py
├── Config: CerebellumConfig
├── Dependencies: NumPy (필수), Hippocampus (선택)
└── Output: correction (보정 신호)
```

---

## 🔌 통합 방식

### 방식 1: PID 제어기 위에 추가 (권장)

```python
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig
import numpy as np

# 소뇌 엔진 초기화
config = CerebellumConfig()
cerebellum = CerebellumEngine(memory_dim=5, config=config)

# 제어 루프
def control_loop(current_state, target_state, velocity, acceleration):
    # 1. PID 제어 (기존)
    error = target_state - current_state
    pid_output = pid_controller.compute(error)
    
    # 2. 소뇌 보정 (추가)
    cerebellum_correction = cerebellum.compute_correction(
        current_state=current_state,
        target_state=target_state,
        velocity=velocity,
        acceleration=acceleration,
        dt=0.001
    )
    
    # 3. 최종 제어 신호
    final_control = pid_output + cerebellum_correction
    
    return final_control
```

**장점**:
- 기존 PID 제어기 유지
- 소뇌만 추가하면 됨
- 안전성 높음 (PID가 기본 제어)

---

### 방식 2: 독립 사용

```python
# 소뇌만 사용 (PID 없이)
correction = cerebellum.compute_correction(...)
control_signal = correction
```

**장점**:
- 단순한 구조
- 빠른 응답

**주의**:
- 기본 안정성은 별도 보장 필요

---

## 🏭 산업 분야별 통합 예시

### 1. 정밀 가공 (5축 CNC)

```python
# CNC 머신 제어
def cnc_control(current_position, target_position, feed_rate):
    # 소뇌 보정
    correction = cerebellum.compute_correction(
        current_state=current_position,
        target_state=target_position,
        context={'tool': 'diamond', 'temperature': machine_temp},
        dt=0.001
    )
    
    # 최종 위치 명령
    corrected_position = target_position + correction
    return corrected_position
```

---

### 2. 로봇 팔 제어

```python
# 로봇 팔 궤적 추적
def robot_arm_control(current_joints, target_joints, velocity):
    # 소뇌 보정
    correction = cerebellum.compute_correction(
        current_state=current_joints,
        target_state=target_joints,
        velocity=velocity,
        context={'payload': payload_weight},
        dt=0.001
    )
    
    # 최종 관절 각도
    corrected_joints = target_joints + correction
    return corrected_joints
```

---

### 3. 항공기 제어

```python
# 자동 조종 시스템
def autopilot_control(current_attitude, target_attitude, airspeed):
    # 소뇌 보정 (공기역학적 지연 보정)
    correction = cerebellum.compute_correction(
        current_state=current_attitude,
        target_state=target_attitude,
        velocity=airspeed,
        context={'altitude': altitude, 'airspeed': airspeed},
        dt=0.01
    )
    
    # 최종 자세 명령
    corrected_attitude = target_attitude + correction
    return corrected_attitude
```

---

## 📊 성능 측정

### 통합 전/후 비교

```python
def measure_improvement():
    # PID만 사용
    pid_only_errors = []
    for trial in range(100):
        error = run_with_pid_only()
        pid_only_errors.append(error)
    
    # PID + Cerebellum
    pid_cb_errors = []
    for trial in range(100):
        error = run_with_pid_and_cerebellum()
        pid_cb_errors.append(error)
    
    # 개선율 계산
    improvement = (np.mean(pid_only_errors) - np.mean(pid_cb_errors)) / np.mean(pid_only_errors) * 100
    return improvement
```

---

## 🔧 최소 통합 요구사항

### 필수
- NumPy 설치
- Python 3.7+

### 선택
- Hippocampus Memory (기억 기반 적응용)
- ROS2 (로봇 통합용)

---

## 💡 핵심 메시지

**소뇌 엔진은 독립적인 모듈로 완성되었습니다.**

- ✅ 전체 엔진 완성 전에도 사용 가능
- ✅ 플러그 앤 플레이 방식
- ✅ 다양한 산업 분야에 적용 가능
- ✅ 최소 의존성

**다음 단계**: 실제 산업 분야에 통합 테스트

---

**업데이트**: 2026-01-22

