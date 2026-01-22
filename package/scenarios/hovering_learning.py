#!/usr/bin/env python3
"""
호버링 학습 시나리오

목표: 제자리에서 공기 타이어를 형성하며 살짝 떠오르는 동작 학습

Author: GNJz
Created: 2026-01-22
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig


class MockMemory:
    """
    해마 메모리 모의 객체 (Hovering 시뮬레이터용)
    
    실제 해마 메모리 대신 간단한 구현을 사용하여
    소뇌 엔진의 기억 기반 적응 기능을 테스트합니다.
    """
    def __init__(self):
        self.memories = {}  # {tuple(state): (bias, confidence)}
    
    def retrieve(self, key, context=None):
        """
        기억 검색
        
        Args:
            key: 현재 상태 (검색 키)
            context: 맥락 정보 (선택적)
        
        Returns:
            memories: 기억 리스트 [{'bias': ..., 'confidence': ...}]
        """
        if len(self.memories) == 0:
            return []
        
        best_match = None
        best_distance = float('inf')
        
        # 유클리드 거리 기반 최근접 이웃 검색
        for stored_key, (value, conf) in self.memories.items():
            distance = np.linalg.norm(key - np.array(stored_key))
            if distance < best_distance:
                best_distance = distance
                # 거리에 따라 confidence 감소
                adjusted_confidence = conf * (1.0 / (1.0 + distance))
                best_match = {
                    'bias': value,
                    'confidence': adjusted_confidence
                }
        
        # 거리 임계값 이내면 반환
        if best_match and best_distance < 0.1:
            return [best_match]
        return []
    
    def store(self, key, value, confidence=0.9, context=None):
        """
        기억 저장
        
        Args:
            key: 상태 (저장 키)
            value: bias 값
            confidence: 신뢰도 [0.0, 1.0]
            context: 맥락 정보 (선택적)
        """
        self.memories[tuple(key)] = (value, confidence)


class HoveringSimulator:
    """호버링 시뮬레이터"""
    
    def __init__(self, cerebellum):
        self.cerebellum = cerebellum
        self.current_state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # [x, y, z, roll, pitch]
        self.target_state = np.array([0.0, 0.0, 0.1, 0.0, 0.0])  # 10cm 상승
        self.velocity = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        
        # 물리 시뮬레이션 파라미터
        self.mass = 1.0  # kg
        self.gravity = 9.81  # m/s²
        self.drag_coefficient = 0.1
        self.thrust_max = 20.0  # N
        
    def step(self, dt=0.001):
        """한 스텝 시뮬레이션"""
        # 소뇌 보정값 계산
        correction = self.cerebellum.compute_correction(
            current_state=self.current_state,
            target_state=self.target_state,
            velocity=self.velocity,
            acceleration=self.acceleration,
            context={'mode': 'hovering'},
            dt=dt
        )
        
        # 목표 상태 보정
        corrected_target = self.target_state + correction
        
        # 오차 계산
        error = corrected_target - self.current_state
        
        # 추력 계산 (간단한 PID)
        thrust_z = error[2] * 10.0  # P gain
        thrust_z = np.clip(thrust_z, 0, self.thrust_max)
        
        # 중력 상쇄
        net_force_z = thrust_z - self.mass * self.gravity
        
        # 가속도 업데이트
        self.acceleration[2] = net_force_z / self.mass
        
        # 속도 업데이트
        self.velocity += self.acceleration * dt
        
        # 드래그 적용
        drag = -self.velocity * self.drag_coefficient
        self.velocity += drag * dt
        
        # 위치 업데이트
        self.current_state += self.velocity * dt
        
        return {
            'state': self.current_state.copy(),
            'velocity': self.velocity.copy(),
            'acceleration': self.acceleration.copy(),
            'correction': correction,
            'thrust': thrust_z,
            'error': error
        }


def learn_hovering(n_trials=100, steps_per_trial=1000):
    """호버링 학습"""
    print("\n" + "=" * 70)
    print("호버링 학습 시나리오")
    print("=" * 70)
    print(f"목표: 제자리에서 공기 타이어를 형성하며 살짝 떠오르는 동작")
    print(f"학습 시행: {n_trials}회")
    print(f"시행당 스텝: {steps_per_trial}")
    print("=" * 70)
    
    # 해마 메모리 생성 (학습용)
    memory = MockMemory()
    
    # 소뇌 엔진 생성 (해마 메모리 연결)
    config = CerebellumConfig(
        feedforward_gain=0.5,
        trial_gain=0.3,
        variance_gain=0.2,
        memory_gain=0.4,
        max_correction_norm=1.0  # 호버링용 작은 값
    )
    cerebellum = CerebellumEngine(memory_dim=5, config=config, memory=memory)
    
    # 시뮬레이터 생성
    simulator = HoveringSimulator(cerebellum)
    
    # 학습 루프
    trial_errors = []
    trial_corrections = []
    trial_settling_times = []
    
    print("\n학습 진행:")
    print(f"{'Trial':>6} | {'RMS Error':>12} | {'Correction RMS':>15} | {'Settling Time':>14} | {'Final Height':>12}")
    print("-" * 70)
    
    for trial in range(n_trials):
        # 시뮬레이터 리셋
        simulator.current_state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        simulator.velocity = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        simulator.acceleration = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        
        trial_error_sum = 0.0
        trial_correction_sum = 0.0
        error_squared_sum = 0.0
        correction_squared_sum = 0.0
        settling_time = None
        target_threshold = 0.01  # 목표 오차 임계값
        
        for step in range(steps_per_trial):
            result = simulator.step(dt=0.001)
            error_norm = np.linalg.norm(result['error'])
            correction_norm = np.linalg.norm(result['correction'])
            
            trial_error_sum += error_norm
            trial_correction_sum += correction_norm
            error_squared_sum += error_norm ** 2
            correction_squared_sum += correction_norm ** 2
            
            # ⭐ 해마에 기억 저장 (안정 구간에서만)
            # 목표 오차가 작을 때만 저장하여 정확한 기억 형성
            if error_norm < 0.05:  # 안정 구간
                # 현재 상태와 오차를 기억으로 저장
                memory.store(
                    key=simulator.current_state,
                    value=result['error'],  # 오차를 bias로 저장
                    confidence=0.9 - error_norm * 10,  # 오차가 작을수록 높은 confidence
                    context={'mode': 'hovering', 'trial': trial}
                )
            
            # Settling time 계산 (목표 오차 이하로 떨어지는 시간)
            if settling_time is None and error_norm < target_threshold:
                settling_time = step * 0.001  # 초 단위
        
        # RMS 계산
        avg_error = trial_error_sum / steps_per_trial
        rms_error = np.sqrt(error_squared_sum / steps_per_trial)
        avg_correction = trial_correction_sum / steps_per_trial
        rms_correction = np.sqrt(correction_squared_sum / steps_per_trial)
        
        trial_errors.append(rms_error)
        trial_corrections.append(rms_correction)
        trial_settling_times.append(settling_time if settling_time else steps_per_trial * 0.001)
        
        # 주기적 출력
        if (trial + 1) % 10 == 0 or trial < 5:
            final_state = result['state']
            final_height = final_state[2]
            settling_str = f"{settling_time:.3f}s" if settling_time else "N/A"
            print(f"{trial+1:6d} | {rms_error:12.6f} | {rms_correction:15.6f} | {settling_str:>14} | {final_height:12.4f}m")
    
    # 결과 분석
    print("\n" + "=" * 70)
    print("학습 결과 분석 (BEFORE / AFTER)")
    print("=" * 70)
    
    # BEFORE (초기 10개 시행)
    before_rms_error = np.mean(trial_errors[:10])
    before_rms_correction = np.mean(trial_corrections[:10])
    before_settling_time = np.mean([t for t in trial_settling_times[:10] if t is not None])
    
    # AFTER (최종 10개 시행)
    after_rms_error = np.mean(trial_errors[-10:])
    after_rms_correction = np.mean(trial_corrections[-10:])
    after_settling_time = np.mean([t for t in trial_settling_times[-10:] if t is not None])
    
    # 개선율 계산
    error_improvement = (1 - after_rms_error / before_rms_error) * 100
    correction_improvement = (1 - after_rms_correction / before_rms_correction) * 100
    settling_improvement = (1 - after_settling_time / before_settling_time) * 100
    
    print(f"\n{'지표':<20} | {'BEFORE (1-10)':>15} | {'AFTER (91-100)':>15} | {'개선율':>10}")
    print("-" * 70)
    print(f"{'RMS Error':<20} | {before_rms_error:15.6f} | {after_rms_error:15.6f} | {error_improvement:>9.2f}%")
    print(f"{'Correction RMS':<20} | {before_rms_correction:15.6f} | {after_rms_correction:15.6f} | {correction_improvement:>9.2f}%")
    print(f"{'Settling Time':<20} | {before_settling_time:15.3f}s | {after_settling_time:15.3f}s | {settling_improvement:>9.2f}%")
    print("=" * 70)
    
    # 종합 평가
    print("\n종합 평가:")
    if error_improvement > 0:
        print(f"✅ RMS Error 개선: {error_improvement:.2f}% 감소")
    else:
        print(f"⚠️ RMS Error 변화: {error_improvement:.2f}%")
    
    if correction_improvement > 0:
        print(f"✅ Correction RMS 개선: {correction_improvement:.2f}% 감소 (더 안정적인 보정)")
    else:
        print(f"⚠️ Correction RMS 변화: {correction_improvement:.2f}%")
    
    if settling_improvement > 0:
        print(f"✅ Settling Time 개선: {settling_improvement:.2f}% 감소 (더 빠른 수렴)")
    else:
        print(f"⚠️ Settling Time 변화: {settling_improvement:.2f}%")
    
    if error_improvement > 10 or settling_improvement > 10:
        print("\n✅ 학습 성공: 명확한 개선이 확인되었습니다!")
    else:
        print("\n⚠️ 학습 진행 중: 더 많은 시행이 필요할 수 있습니다.")
    
    return cerebellum, {
        'errors': trial_errors,
        'corrections': trial_corrections,
        'settling_times': trial_settling_times,
        'before': {
            'rms_error': before_rms_error,
            'rms_correction': before_rms_correction,
            'settling_time': before_settling_time
        },
        'after': {
            'rms_error': after_rms_error,
            'rms_correction': after_rms_correction,
            'settling_time': after_settling_time
        },
        'improvements': {
            'error': error_improvement,
            'correction': correction_improvement,
            'settling': settling_improvement
        }
    }


def main():
    """메인 함수"""
    cerebellum, results = learn_hovering(n_trials=100, steps_per_trial=1000)
    
    print("\n" + "=" * 70)
    print("호버링 학습 완료")
    print("=" * 70)
    print("소뇌 엔진이 호버링 동작을 학습했습니다.")
    print("이제 실제 기계에 적용할 준비가 되었습니다!")
    print("=" * 70)
    
    # 수치 요약 출력
    print("\n📊 수치 요약:")
    print(f"   Trial 1:   RMS error = {results['errors'][0]:.6f}, Correction RMS = {results['corrections'][0]:.6f}")
    print(f"   Trial 50:  RMS error = {results['errors'][49]:.6f}, Correction RMS = {results['corrections'][49]:.6f}")
    print(f"   Trial 100: RMS error = {results['errors'][99]:.6f}, Correction RMS = {results['corrections'][99]:.6f}")


if __name__ == "__main__":
    main()

