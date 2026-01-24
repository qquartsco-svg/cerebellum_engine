"""
Cerebellum Engine
소뇌(Cerebellum) 엔진 - 기억을 즉각 행동으로 변환하는 계층 (소프트웨어 벤치마킹 단계)

⚠️ 현재 상태:
- 소프트웨어 시뮬레이션 및 벤치마킹 단계
- 맥북에어에서 간단한 소프트웨어 테스트 후 업로드
- 물리적 하드웨어 테스트는 아직 완료되지 않음
- 계속 발전하는 구조 (테스트 과정과 계획된 업그레이드로 확장)

================================================================================
핵심 개념 및 수식
================================================================================

1. Predictive Feedforward (예측 피드포워드)
   수식: e_pred(t+Δt) = e(t) + v(t)·Δt + ½a(t)·(Δt)²
   의미: 다음 순간의 오차를 미리 예측하여 사전 보정
   생물학적 대응: 소뇌의 Internal Model (내부 모델)

2. Trial-to-Trial 보정 (회차 학습)
   수식: trial_error = e(t) - b_hip(x(t), c(t))
         trial_correction = -trial_error · α_trial
   의미: 반복 궤적에서 항상 생기던 오차를 기억하고 다음 시행에서 제거
   생물학적 대응: 소뇌의 Trial-to-Trial Learning

3. Variance 감소 (떨림 필터링)
   수식: high_freq_noise = e(t) - filtered_error
         variance_correction = -high_freq_noise · α_variance
   의미: 고주파 노이즈(떨림) 제거, 저주파 의도적 움직임 유지
   생물학적 대응: 소뇌의 Tremor Suppression

4. 기억 기반 적응 (해마 연동)
   수식: memory_correction = -b_hip(x(t), c(t)) · α_memory · confidence · context_weight
   의미: 해마의 기억을 즉각 행동으로 변환
   생물학적 대응: Hippocampus → Cerebellum 연결

5. 최종 보정 신호 (통합)
   수식: u_cb(t) = (u_ff + u_trial + u_variance + u_memory) · w_total
   의미: 모든 보정 신호를 통합하여 최종 보정값 생성

6. Saturation (포화 제한) - v0.6
   수식: if ||u_cb|| > max_norm:
             u_cb = u_cb · (max_norm / ||u_cb||)
   의미: 과도한 보정 신호 방지, 안정성 확보

================================================================================
버전 이력
================================================================================
- v0.5.0-alpha: 기본 기능 구현 (Predictive Feedforward, Trial-to-Trial, Variance 감소)
- v0.6.0-beta: 안정성 기능 추가 (Confidence gain, Saturation, Context weight)

Author: GNJz
Created: 2026-01-20
Updated: 2026-01-22 (v0.6.0-beta)
Made in GNJz
License: MIT License
"""

from typing import Dict, Any, Optional, List
import numpy as np
from collections import deque
from dataclasses import dataclass, field


@dataclass
class CerebellumConfig:
    """소뇌 설정"""
    # Predictive Feedforward
    feedforward_gain: float = 0.5  # 피드포워드 gain
    prediction_horizon: float = 0.01  # 예측 시간 (초)
    
    # Trial-to-Trial 보정
    trial_gain: float = 0.3  # Trial 보정 gain
    
    # Variance 감소
    variance_gain: float = 0.2  # Variance 감소 gain
    low_pass_cutoff: float = 10.0  # 저주파 필터 차단 주파수 (Hz)
    variance_window: int = 5  # 분산 계산 윈도우 크기
    
    # 기억 기반 적응
    memory_gain: float = 0.4  # 기억 기반 보정 gain
    
    # 통합
    correction_weight: float = 1.0  # 전체 보정 가중치
    
    # ⭐ v0.6 추가: 안정성 파라미터
    max_correction_norm: float = 10.0  # 최대 보정 신호 크기 (saturation)
    min_confidence: float = 0.1  # 최소 신뢰도 (confidence 기반 gain)
    context_weight_enabled: bool = True  # Context 가중치 사용 여부


class CerebellumEngine:
    """
    소뇌 엔진
    
    해마의 기억을 즉각 행동으로 변환하는 계층 (소프트웨어 벤치마킹 단계)
    
    ⚠️ 현재 상태:
    - 소프트웨어 시뮬레이션 단계
    - 물리적 하드웨어 테스트 미완
    - 계속 발전하는 구조
    
    예상 역할:
    1. Predictive Feedforward: 다음 순간의 오차 예측
    2. Trial-to-Trial 보정: 반복 궤적의 미세 편차 제거
    3. Variance 감소: 미세한 떨림 필터링
    4. 기억 기반 적응: 해마의 기억을 즉각 행동으로 변환
    """
    
    def __init__(
        self,
        memory_dim: int = 5,
        config: Optional[CerebellumConfig] = None,
        memory: Optional[Any] = None  # UniversalMemory 인스턴스
    ):
        """
        소뇌 엔진 초기화
        
        Args:
            memory_dim: 메모리 차원 (기본값: 5D)
            config: 소뇌 설정 (None이면 기본값)
            memory: 해마 메모리 인스턴스 (None이면 나중에 설정)
        """
        self.memory_dim = memory_dim
        self.config = config or CerebellumConfig()
        self.memory = memory
        
        # 상태 기록 (Variance 감소용)
        self.error_history: deque = deque(maxlen=self.config.variance_window)
        self.state_history: deque = deque(maxlen=self.config.variance_window)
        
        # 이전 상태 (예측용)
        self.prev_state: Optional[np.ndarray] = None
        self.prev_velocity: Optional[np.ndarray] = None
        self.prev_time: float = 0.0
        
        # 저주파 필터 상태 (Variance 감소용)
        self.filtered_error: Optional[np.ndarray] = None
    
    def set_memory(self, memory: Any) -> None:
        """
        해마 메모리 설정
        
        Args:
            memory: UniversalMemory 인스턴스
        """
        self.memory = memory
    
    def compute_correction(
        self,
        current_state: np.ndarray,
        target_state: np.ndarray,
        velocity: Optional[np.ndarray] = None,
        acceleration: Optional[np.ndarray] = None,
        context: Optional[Dict[str, Any]] = None,
        dt: float = 0.001  # 시간 간격 (초, 기본값: 1ms)
    ) -> np.ndarray:
        """
        소뇌 보정값 계산
        
        해마의 기억을 활용하여 즉각 보정값을 계산합니다.
        
        Args:
            current_state: 현재 상태 [x, y, z, theta_a, theta_b]
            target_state: 목표 상태 [x, y, z, theta_a, theta_b]
            velocity: 현재 속도 (None이면 계산)
            acceleration: 현재 가속도 (None이면 계산)
            context: 맥락 정보 (해마 메모리 검색용)
            dt: 시간 간격 (초)
        
        Returns:
            cerebellum_correction: 소뇌 보정값 [x, y, z, theta_a, theta_b]
        """
        # 현재 오차 계산
        current_error = target_state - current_state
        
        # 상태 기록 업데이트
        self.error_history.append(current_error.copy())
        self.state_history.append(current_state.copy())
        
        # 속도/가속도 계산 (제공되지 않은 경우)
        if velocity is None:
            velocity = self._estimate_velocity(current_state, dt)
        if acceleration is None:
            acceleration = self._estimate_acceleration(velocity, dt)
        
        # 1. 해마에서 기억 검색 (기억 기반 적응) - v0.6: confidence 포함
        memory_bias, confidence = self._get_memory_bias(current_state, context)
        
        # ⭐ v0.6: Confidence 기반 adaptive gain 계산
        adaptive_gain = self._compute_adaptive_gain(confidence)
        
        # ⭐ v0.6: Context 가중치 계산
        context_weight = self._compute_context_weight(context) if self.config.context_weight_enabled else 1.0
        
        # 2. Predictive Feedforward (다음 순간의 오차 예측)
        predicted_error = self._predict_error(
            current_error,
            velocity,
            acceleration,
            dt
        )
        feedforward_correction = -predicted_error * self.config.feedforward_gain
        
        # 3. Trial-to-Trial 보정 (반복 궤적의 미세 편차 제거)
        trial_correction = self._compute_trial_correction(
            current_error,
            memory_bias
        )
        
        # 4. Variance 감소 (미세한 떨림 필터링)
        variance_correction = self._reduce_variance(current_error)
        
        # 5. 기억 기반 적응 (해마의 기억을 즉각 행동으로 변환)
        # ⭐ v0.6: confidence와 context_weight 적용
        memory_correction = -memory_bias * self.config.memory_gain * adaptive_gain * context_weight
        
        # 6. 통합 보정
        total_correction = (
            feedforward_correction +
            trial_correction +
            variance_correction +
            memory_correction
        ) * self.config.correction_weight
        
        # ⭐ v0.6: Error norm 기반 saturation 적용
        total_correction = self._saturate_correction(total_correction)
        
        # 이전 상태 업데이트
        self.prev_state = current_state.copy()
        self.prev_velocity = velocity.copy()
        
        return total_correction
    
    def _get_memory_bias(
        self,
        current_state: np.ndarray,
        context: Optional[Dict[str, Any]]
    ) -> tuple:
        """
        해마 메모리에서 기억된 bias 검색 (v0.6: confidence 반환)
        
        Args:
            current_state: 현재 상태
            context: 맥락 정보
        
        Returns:
            (memory_bias, confidence): 기억된 bias와 신뢰도 (없으면 0 벡터, 0.0)
        """
        if self.memory is None:
            return np.zeros(self.memory_dim), 0.0
        
        try:
            # 해마 메모리에서 기억 검색
            memories = self.memory.retrieve(current_state, context or {})
            
            if memories:
                # 첫 번째 기억의 bias와 confidence 사용
                memory_bias = memories[0].get('bias', np.zeros(self.memory_dim))
                confidence = memories[0].get('confidence', 0.5)  # 기본값 0.5
                # confidence를 [min_confidence, 1.0] 범위로 클리핑
                confidence = np.clip(confidence, self.config.min_confidence, 1.0)
                return memory_bias, confidence
            else:
                return np.zeros(self.memory_dim), 0.0
        except Exception:
            # 오류 발생 시 0 벡터 반환
            return np.zeros(self.memory_dim), 0.0
    
    def _predict_error(
        self,
        current_error: np.ndarray,
        velocity: np.ndarray,
        acceleration: np.ndarray,
        dt: float
    ) -> np.ndarray:
        """
        다음 순간의 오차 예측 (Predictive Feedforward)
        
        ================================================================================
        수식 설명
        ================================================================================
        e_pred(t+Δt) = e(t) + v(t)·Δt + ½a(t)·(Δt)²
        
        여기서:
        - e(t): 현재 오차 (current_error)
        - v(t): 현재 속도 (velocity)
        - a(t): 현재 가속도 (acceleration)
        - Δt: 예측 시간 (prediction_horizon)
        - e_pred(t+Δt): 예측된 오차
        
        물리적 의미:
        - 현재 오차에 속도와 가속도를 고려하여 다음 순간의 오차를 예측
        - Taylor 전개 1차 항(속도) + 2차 항(가속도) 사용
        
        생물학적 대응:
        - 소뇌의 Internal Model (내부 모델)
        - Forward Model을 통한 오차 예측
        
        ================================================================================
        
        Args:
            current_error: 현재 오차 [x, y, z, theta_a, theta_b]
            velocity: 현재 속도 [vx, vy, vz, v_theta_a, v_theta_b]
            acceleration: 현재 가속도 [ax, ay, az, a_theta_a, a_theta_b]
            dt: 시간 간격 (초) - 실제로는 prediction_horizon 사용
        
        Returns:
            predicted_error: 예측된 오차 [x, y, z, theta_a, theta_b]
        """
        # 예측 시간
        prediction_dt = self.config.prediction_horizon
        
        # 예측 오차 계산
        predicted_error = (
            current_error +
            velocity * prediction_dt +
            0.5 * acceleration * prediction_dt ** 2
        )
        
        return predicted_error
    
    def _compute_trial_correction(
        self,
        current_error: np.ndarray,
        memory_bias: np.ndarray
    ) -> np.ndarray:
        """
        Trial-to-Trial 보정 계산
        
        ================================================================================
        수식 설명
        ================================================================================
        trial_error = e(t) - b_hip(x(t), c(t))
        trial_correction = -trial_error · α_trial
        
        여기서:
        - e(t): 현재 오차 (current_error)
        - b_hip(x(t), c(t)): 해마에서 기억된 bias (memory_bias)
        - trial_error: Trial 오차 (기억된 bias와 현재 오차의 차이)
        - α_trial: Trial gain (trial_gain)
        - trial_correction: Trial 보정값
        
        의미:
        - 반복 궤적에서 "항상 생기던 오차"를 기억하고
        - 다음 시행에서 미리 제거하여 더 정확한 제어
        
        생물학적 대응:
        - 소뇌의 Trial-to-Trial Learning
        - 인간이 악기·운동 배울 때 정확히 이 방식
        
        ================================================================================
        
        Args:
            current_error: 현재 오차 [x, y, z, theta_a, theta_b]
            memory_bias: 기억된 bias [bx, by, bz, b_theta_a, b_theta_b]
        
        Returns:
            trial_correction: Trial 보정값 [x, y, z, theta_a, theta_b]
        """
        # Trial 오차 계산 (기억된 bias와 현재 오차의 차이)
        trial_error = current_error - memory_bias
        
        # Trial 보정
        trial_correction = -trial_error * self.config.trial_gain
        
        return trial_correction
    
    def _reduce_variance(
        self,
        current_error: np.ndarray
    ) -> np.ndarray:
        """
        Variance 감소 (미세한 떨림 필터링)
        
        ================================================================================
        수식 설명
        ================================================================================
        filtered_error = mean(error_history)  # 이동 평균 필터
        high_freq_noise = e(t) - filtered_error
        variance_correction = -high_freq_noise · α_variance
        
        여기서:
        - e(t): 현재 오차 (current_error)
        - filtered_error: 저주파 필터링된 오차 (이동 평균)
        - high_freq_noise: 고주파 노이즈 (떨림)
        - α_variance: Variance gain (variance_gain)
        - variance_correction: Variance 감소 보정값
        
        의미:
        - 고주파 노이즈(떨림) 제거
        - 저주파 의도적 움직임 유지
        - 분산(Variance) 감소
        
        생물학적 대응:
        - 소뇌의 Tremor Suppression
        - 파킨슨·소뇌 실조 연구에도 쓰는 개념
        
        ================================================================================
        
        Args:
            current_error: 현재 오차 [x, y, z, theta_a, theta_b]
        
        Returns:
            variance_correction: Variance 감소 보정값 [x, y, z, theta_a, theta_b]
        """
        # 저주파 필터 적용 (단순 이동 평균)
        if len(self.error_history) < self.config.variance_window:
            # 윈도우가 채워지지 않았으면 현재 오차 사용
            filtered_error = current_error.copy()
        else:
            # 이동 평균 필터
            error_array = np.array(list(self.error_history))
            filtered_error = np.mean(error_array, axis=0)
        
        # 필터링된 오차 저장
        self.filtered_error = filtered_error
        
        # Variance 보정 (고주파 노이즈 제거)
        high_freq_noise = current_error - filtered_error
        variance_correction = -high_freq_noise * self.config.variance_gain
        
        return variance_correction
    
    def _compute_adaptive_gain(self, confidence: float) -> float:
        """
        Confidence 기반 adaptive gain 계산 (v0.6)
        
        기억이 확실할수록 강하게, 불확실하면 소극적으로 보정
        
        Args:
            confidence: 해마 메모리의 신뢰도 [0.0, 1.0]
        
        Returns:
            adaptive_gain: 적응형 gain [min_confidence, 1.0]
        """
        # confidence를 [min_confidence, 1.0] 범위로 정규화
        adaptive_gain = np.clip(confidence, self.config.min_confidence, 1.0)
        return adaptive_gain
    
    def _compute_context_weight(self, context: Optional[Dict[str, Any]]) -> float:
        """
        Context 가중치 계산 (v0.6)
        
        같은 위치라도 상황(context)이 다르면 소뇌 반응이 달라야 함
        
        Args:
            context: 맥락 정보 (tool, temperature, medium 등)
        
        Returns:
            context_weight: 맥락 가중치 [0.0, 1.0]
        """
        if context is None or len(context) == 0:
            return 0.5  # 맥락 없으면 중간 가중치
        
        # 간단한 구현: 맥락 키 개수 기반 가중치
        # 실제로는 맥락 일치도 계산 필요
        context_weight = min(1.0, 0.5 + len(context) * 0.1)
        return context_weight
    
    def _saturate_correction(self, correction: np.ndarray) -> np.ndarray:
        """
        Error norm 기반 saturation (v0.6)
        
        ================================================================================
        수식 설명
        ================================================================================
        if ||u_cb|| > max_norm:
            u_cb = u_cb · (max_norm / ||u_cb||)
        else:
            u_cb = u_cb
        
        여기서:
        - u_cb: 보정 신호 (correction)
        - ||u_cb||: 보정 신호의 노름 (L2 norm)
        - max_norm: 최대 보정 신호 크기 (max_correction_norm)
        
        의미:
        - 큰 오차 + feedforward + trial + variance가 겹치면 순간 과출력 방지
        - 안정성 확보
        - 실기계/로봇 투입 가능
        
        ================================================================================
        
        Args:
            correction: 보정 신호 [x, y, z, theta_a, theta_b]
        
        Returns:
            saturated_correction: 포화 제한된 보정 신호 [x, y, z, theta_a, theta_b]
        """
        correction_norm = np.linalg.norm(correction)
        max_norm = self.config.max_correction_norm
        
        if correction_norm > max_norm:
            # Soft saturation: smooth clip
            eps = 1e-8
            scale = max_norm / (correction_norm + eps)
            return correction * scale
        
        return correction
    
    def _estimate_velocity(
        self,
        current_state: np.ndarray,
        dt: float
    ) -> np.ndarray:
        """
        속도 추정 (이전 상태 기반)
        
        Args:
            current_state: 현재 상태
            dt: 시간 간격
        
        Returns:
            velocity: 추정된 속도
        """
        if self.prev_state is None or dt <= 0:
            return np.zeros(self.memory_dim)
        
        velocity = (current_state - self.prev_state) / dt
        return velocity
    
    def _estimate_acceleration(
        self,
        velocity: np.ndarray,
        dt: float
    ) -> np.ndarray:
        """
        가속도 추정 (이전 속도 기반)
        
        Args:
            velocity: 현재 속도
            dt: 시간 간격
        
        Returns:
            acceleration: 추정된 가속도
        """
        if self.prev_velocity is None or dt <= 0:
            return np.zeros(self.memory_dim)
        
        acceleration = (velocity - self.prev_velocity) / dt
        return acceleration
    
    def reset(self) -> None:
        """소뇌 엔진 리셋"""
        self.error_history.clear()
        self.state_history.clear()
        self.prev_state = None
        self.prev_velocity = None
        self.filtered_error = None


# 편의 함수: 소뇌 엔진 생성
def create_cerebellum_engine(
    memory_dim: int = 5,
    config: Optional[CerebellumConfig] = None,
    memory: Optional[Any] = None
) -> CerebellumEngine:
    """
    소뇌 엔진 생성 (편의 함수)
    
    Args:
        memory_dim: 메모리 차원
        config: 소뇌 설정
        memory: 해마 메모리 인스턴스
    
    Returns:
        CerebellumEngine 인스턴스
    """
    return CerebellumEngine(
        memory_dim=memory_dim,
        config=config,
        memory=memory
    )

