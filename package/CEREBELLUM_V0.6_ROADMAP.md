# 소뇌 엔진 v0.6 로드맵

**현재 버전**: v0.5.0-alpha  
**목표 버전**: v0.6.0-beta  
**상태**: 피드백 기반 개선 계획

---

## 🎯 v0.6 핵심 개선 사항

### 1. Confidence 기반 Gain 조절

**문제**: Trial gain / variance gain 동시 적용 시 특정 상황에서 correction이 커질 수 있음

**해결책**:
```python
def _compute_adaptive_gain(self, error_norm, confidence):
    """오차 크기와 신뢰도 기반 적응형 gain"""
    # 오차가 클 때는 보수적으로
    if error_norm > self.config.max_error_threshold:
        scale = 0.5
    else:
        scale = 1.0
    
    # 신뢰도 기반 조절
    confidence_scale = confidence if confidence else 0.5
    
    return scale * confidence_scale
```

### 2. Error Norm 기반 Saturation

**문제**: 과도한 보정 신호 방지

**해결책**:
```python
def _saturate_correction(self, correction, max_norm):
    """보정 신호 포화 제한"""
    correction_norm = np.linalg.norm(correction)
    if correction_norm > max_norm:
        return correction * (max_norm / correction_norm)
    return correction
```

### 3. Context 기반 메모리 가중치

**문제**: 맥락에 따른 메모리 신뢰도 차이

**해결책**:
```python
def _get_contextual_memory_weight(self, context, memory_context):
    """맥락 일치도 기반 가중치"""
    if not context or not memory_context:
        return 0.5
    
    # 맥락 일치도 계산
    match_score = self._compute_context_match(context, memory_context)
    return match_score
```

---

## 🔬 추가 연구 방향

### 1. 학습률 적응 (Adaptive Learning Rate)

- Trial-to-Trial 보정의 학습률을 동적으로 조절
- 수렴 속도와 안정성 균형

### 2. 다중 시간 스케일 통합

- 단기: Predictive Feedforward
- 중기: Trial-to-Trial
- 장기: 해마 메모리

### 3. 불확실성 정량화

- 보정 신호의 불확실성 추정
- 신뢰 구간 제공

---

## 📊 벤치마크 계획

### 1. 로봇 팔 제어 시뮬레이션

- 5축 로봇 팔 궤적 추적
- PID vs PID + Cerebellum 비교

### 2. 정밀 가공 시뮬레이션

- 0.00001 단위 정밀도 요구
- 열팽창, 진동 보정

### 3. 항공기 제어 시뮬레이션

- 공기역학적 지연 보정
- 터보팬 엔진 제어

---

## 🚀 실제 적용 시나리오

### 시나리오 1: 호버링 (Hovering) 학습

**목표**: 제자리에서 공기 타이어를 형성하며 살짝 떠오르는 동작

**구현**:
```python
# 호버링 궤적 정의
hovering_trajectory = {
    'position': [0.0, 0.0, 0.1],  # 10cm 상승
    'velocity': [0.0, 0.0, 0.0],  # 정지
    'acceleration': [0.0, 0.0, 0.0]
}

# 소뇌에 학습
for trial in range(100):
    correction = cerebellum.compute_correction(
        current_state=current_state,
        target_state=hovering_trajectory['position'],
        velocity=hovering_trajectory['velocity'],
        acceleration=hovering_trajectory['acceleration'],
        context={'mode': 'hovering'},
        dt=0.001
    )
    # 제어 루프 실행
```

### 시나리오 2: 기류 제어 (0.00001 정밀도)

**목표**: 기어가 0.00001 차이로 공기만 통과시킬 때 실시간 간극 조정

**구현**:
```python
# 초정밀 기류 제어
airflow_control = {
    'target_gap': 0.00001,  # 10 마이크론
    'tolerance': 0.000001,  # 1 마이크론
    'context': {'temperature': temp, 'pressure': pressure}
}

correction = cerebellum.compute_correction(
    current_state=current_gap,
    target_state=airflow_control['target_gap'],
    context=airflow_control['context'],
    dt=0.0001  # 매우 빠른 샘플링
)
```

### 시나리오 3: 다이아몬드 코팅면 보호

**목표**: 미세 떨림 제거로 마모 방지

**구현**:
```python
# Variance 감소 강화
config = CerebellumConfig(
    variance_gain=0.3,  # 높은 필터링
    variance_window=10,  # 긴 윈도우
    low_pass_cutoff=5.0  # 낮은 차단 주파수
)

cerebellum = CerebellumEngine(config=config)
```

---

## 📝 문서화 계획

### 1. API 레퍼런스

- 모든 메서드 상세 설명
- 파라미터 타입 및 범위
- 반환값 설명

### 2. 사용 예제 모음

- 기본 사용법
- 고급 통합 예제
- 실제 적용 사례

### 3. 성능 벤치마크 리포트

- 다양한 시나리오 성능 측정
- PID 대비 개선율
- 계산 복잡도 분석

---

## 🎯 v0.6 릴리즈 기준

- [ ] Confidence 기반 gain 조절 구현
- [ ] Error norm 기반 saturation 구현
- [ ] Context 기반 메모리 가중치 구현
- [ ] 호버링 학습 시나리오 완성
- [ ] 벤치마크 리포트 작성
- [ ] API 문서화 완료

---

**예상 릴리즈**: 2026-02

