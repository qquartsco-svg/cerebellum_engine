# 소뇌 엔진 - 독립 모듈

**버전**: v0.6.0-beta  
**상태**: 산업 적용 가능

---

## 🎯 핵심 원칙

**모듈화 & 핵심 부품화**

- ✅ 독립적인 모듈로 완성
- ✅ 전체 엔진(쿠키 브레인) 완성 전에도 사용 가능
- ✅ 플러그 앤 플레이 방식
- ✅ 최소 의존성 (NumPy만 필요)

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

4. **자율주행 차량**
   - 차선 유지
   - 자동 주차

5. **의료 기기**
   - 정밀 주사기
   - 수술 로봇

6. **반도체 제조**
   - 웨이퍼 정렬
   - 마스크 정렬

---

## 🔌 빠른 시작

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

## 📊 성능 지표

- **정밀도 향상**: RMS Error 감소율
- **안정성 향상**: Variance 감소율
- **학습 효과**: Trial-to-Trial 개선율

---

## 📝 문서

- `INDUSTRIAL_APPLICATIONS.md`: 산업 적용 분야 상세
- `MODULE_INTEGRATION_GUIDE.md`: 통합 가이드
- `examples/`: 산업 분야별 예시 코드

---

**핵심**: 소뇌 엔진은 독립적인 모듈로 완성되었습니다.

