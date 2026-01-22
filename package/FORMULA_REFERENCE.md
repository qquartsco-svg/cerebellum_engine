# 소뇌 엔진 수식 참조 가이드

**버전**: v0.6.0-beta  
**작성일**: 2026-01-22

---

## 📐 핵심 수식 모음

### 1. Predictive Feedforward (예측 피드포워드)

**수식**:
\[
e_{\text{pred}}(t+\Delta t) = e(t) + v(t) \cdot \Delta t + \frac{1}{2} a(t) \cdot (\Delta t)^2
\]

**변수 설명**:
- \(e(t)\): 현재 오차 (current_error)
- \(v(t)\): 현재 속도 (velocity)
- \(a(t)\): 현재 가속도 (acceleration)
- \(\Delta t\): 예측 시간 (prediction_horizon)
- \(e_{\text{pred}}(t+\Delta t)\): 예측된 오차

**물리적 의미**:
- Taylor 전개 1차 항(속도) + 2차 항(가속도) 사용
- 현재 오차에 속도와 가속도를 고려하여 다음 순간의 오차를 예측

**생물학적 대응**:
- 소뇌의 Internal Model (내부 모델)
- Forward Model을 통한 오차 예측

---

### 2. Trial-to-Trial 보정 (회차 학습)

**수식**:
\[
e_{\text{trial}} = e(t) - b_{\text{hip}}(x(t), c(t))
\]
\[
u_{\text{trial}} = -e_{\text{trial}} \cdot \alpha_{\text{trial}}
\]

**변수 설명**:
- \(e(t)\): 현재 오차 (current_error)
- \(b_{\text{hip}}(x(t), c(t))\): 해마에서 기억된 bias (memory_bias)
- \(e_{\text{trial}}\): Trial 오차 (기억된 bias와 현재 오차의 차이)
- \(\alpha_{\text{trial}}\): Trial gain (trial_gain)
- \(u_{\text{trial}}\): Trial 보정값

**의미**:
- 반복 궤적에서 "항상 생기던 오차"를 기억하고
- 다음 시행에서 미리 제거하여 더 정확한 제어

**생물학적 대응**:
- 소뇌의 Trial-to-Trial Learning
- 인간이 악기·운동 배울 때 정확히 이 방식

---

### 3. Variance 감소 (떨림 필터링)

**수식**:
\[
e_{\text{filtered}} = \text{mean}(\text{error\_history}) \quad \text{(이동 평균 필터)}
\]
\[
n_{\text{high\_freq}} = e(t) - e_{\text{filtered}}
\]
\[
u_{\text{variance}} = -n_{\text{high\_freq}} \cdot \alpha_{\text{variance}}
\]

**변수 설명**:
- \(e(t)\): 현재 오차 (current_error)
- \(e_{\text{filtered}}\): 저주파 필터링된 오차 (이동 평균)
- \(n_{\text{high\_freq}}\): 고주파 노이즈 (떨림)
- \(\alpha_{\text{variance}}\): Variance gain (variance_gain)
- \(u_{\text{variance}}\): Variance 감소 보정값

**의미**:
- 고주파 노이즈(떨림) 제거
- 저주파 의도적 움직임 유지
- 분산(Variance) 감소

**생물학적 대응**:
- 소뇌의 Tremor Suppression
- 파킨슨·소뇌 실조 연구에도 쓰는 개념

---

### 4. 기억 기반 적응 (해마 연동)

**수식**:
\[
u_{\text{memory}} = -b_{\text{hip}}(x(t), c(t)) \cdot \alpha_{\text{memory}} \cdot \text{confidence} \cdot \text{context\_weight}
\]

**변수 설명**:
- \(b_{\text{hip}}(x(t), c(t))\): 해마에서 기억된 bias (memory_bias)
- \(\alpha_{\text{memory}}\): Memory gain (memory_gain)
- \(\text{confidence}\): 해마 메모리의 신뢰도 [0.0, 1.0]
- \(\text{context\_weight}\): 맥락 가중치 [0.0, 1.0]
- \(u_{\text{memory}}\): 기억 기반 보정값

**의미**:
- 해마의 기억을 즉각 행동으로 변환
- confidence와 context에 따라 가중치 조절

**생물학적 대응**:
- Hippocampus → Cerebellum 연결
- 기억을 즉각 행동으로 변환하는 계층

---

### 5. 최종 보정 신호 (통합)

**수식**:
\[
u_{\text{cb}}(t) = (u_{\text{ff}} + u_{\text{trial}} + u_{\text{variance}} + u_{\text{memory}}) \cdot w_{\text{total}}
\]

**변수 설명**:
- \(u_{\text{ff}}\): Feedforward 보정값
- \(u_{\text{trial}}\): Trial 보정값
- \(u_{\text{variance}}\): Variance 보정값
- \(u_{\text{memory}}\): Memory 보정값
- \(w_{\text{total}}\): 전체 보정 가중치 (correction_weight)
- \(u_{\text{cb}}(t)\): 최종 소뇌 보정값

**의미**:
- 모든 보정 신호를 통합하여 최종 보정값 생성

---

### 6. Saturation (포화 제한) - v0.6

**수식**:
\[
\text{if } ||u_{\text{cb}}|| > \text{max\_norm}:
\]
\[
\quad u_{\text{cb}} = u_{\text{cb}} \cdot \frac{\text{max\_norm}}{||u_{\text{cb}}||}
\]
\[
\text{else:}
\]
\[
\quad u_{\text{cb}} = u_{\text{cb}}
\]

**변수 설명**:
- \(u_{\text{cb}}\): 보정 신호 (correction)
- \(||u_{\text{cb}}||\): 보정 신호의 노름 (L2 norm)
- \(\text{max\_norm}\): 최대 보정 신호 크기 (max_correction_norm)

**의미**:
- 큰 오차 + feedforward + trial + variance가 겹치면 순간 과출력 방지
- 안정성 확보
- 실기계/로봇 투입 가능

---

## 🔗 수식 간 관계

```
현재 오차 e(t)
    ↓
[1. Predictive Feedforward] → u_ff
    ↓
[2. Trial-to-Trial] → u_trial
    ↓
[3. Variance 감소] → u_variance
    ↓
[4. 기억 기반 적응] → u_memory
    ↓
[5. 통합] → u_cb
    ↓
[6. Saturation] → 최종 보정값
```

---

## 📚 참고 문헌

- 소뇌의 Internal Model: Kawato et al. (1987)
- Trial-to-Trial Learning: Shadmehr & Mussa-Ivaldi (1994)
- Tremor Suppression: Miall et al. (1993)

---

**업데이트**: 2026-01-22

