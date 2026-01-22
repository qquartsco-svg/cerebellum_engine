# 빠른 시작 가이드

## 설치

```bash
cd package
pip install numpy
```

## 기본 사용

```python
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig
import numpy as np

# 소뇌 엔진 생성
engine = CerebellumEngine(memory_dim=5)

# 보정값 계산
correction = engine.compute_correction(
    current_state=np.array([0.0, 0.0, 0.0, 0.0, 0.0]),
    target_state=np.array([1.0, 1.0, 0.0, 0.0, 0.0]),
    dt=0.001
)
```

## 테스트

```bash
python3 run_all_tests.py
```

## 예시 실행

```bash
# 정밀 가공
python3 examples/precision_machining_example.py

# 로봇 팔
python3 examples/robot_arm_example.py

# 항공기
python3 examples/aircraft_control_example.py
```

