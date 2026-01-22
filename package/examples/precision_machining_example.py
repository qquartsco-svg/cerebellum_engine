#!/usr/bin/env python3
"""
정밀 가공 시나리오 예시

5축 CNC 머신에서 소뇌 엔진을 사용한 정밀 가공 제어

Author: GNJz
Created: 2026-01-22
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig


class SimplePID:
    """간단한 PID 제어기"""
    def __init__(self, kp=1.0, ki=0.1, kd=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = np.zeros(5)
        self.prev_error = None
    
    def compute(self, error, dt=0.001):
        """PID 제어 신호 계산"""
        if self.prev_error is None:
            self.prev_error = error.copy()
        
        p_term = self.kp * error
        self.integral += error * dt
        i_term = self.ki * self.integral
        d_term = self.kd * (error - self.prev_error) / dt
        self.prev_error = error.copy()
        
        return p_term + i_term + d_term


class PrecisionMachiningController:
    """정밀 가공 제어기 (PID + Cerebellum)"""
    
    def __init__(self):
        # PID 제어기
        self.pid = SimplePID(kp=1.0, ki=0.1, kd=0.05)
        
        # 소뇌 엔진
        config = CerebellumConfig(
            feedforward_gain=0.5,
            trial_gain=0.3,
            variance_gain=0.2,
            memory_gain=0.4,
            max_correction_norm=1.0  # 정밀 가공용 작은 값
        )
        self.cerebellum = CerebellumEngine(memory_dim=5, config=config)
        
        # 상태 추적
        self.current_position = np.array([0.0, 0.0, 0.0, 0.0, 0.0])  # [x, y, z, A, C]
        self.velocity = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    
    def control_step(self, target_position, dt=0.001, context=None):
        """
        한 스텝 제어
        
        Args:
            target_position: 목표 위치 [x, y, z, A, C]
            dt: 시간 간격
            context: 맥락 정보 (tool, temperature 등)
        
        Returns:
            control_signal: 제어 신호
        """
        # 오차 계산
        error = target_position - self.current_position
        
        # 1. PID 제어 (기본 제어)
        pid_output = self.pid.compute(error, dt)
        
        # 2. 소뇌 보정 (정밀 보정)
        cerebellum_correction = self.cerebellum.compute_correction(
            current_state=self.current_position,
            target_state=target_position,
            velocity=self.velocity,
            acceleration=self.acceleration,
            context=context or {},
            dt=dt
        )
        
        # 3. 최종 제어 신호 (PID + Cerebellum)
        final_control = pid_output + cerebellum_correction
        
        # 상태 업데이트 (시뮬레이션)
        self.current_position += final_control * dt
        self.velocity = (self.current_position - self.prev_position) / dt if hasattr(self, 'prev_position') else np.zeros(5)
        self.acceleration = (self.velocity - self.prev_velocity) / dt if hasattr(self, 'prev_velocity') else np.zeros(5)
        
        self.prev_position = self.current_position.copy()
        self.prev_velocity = self.velocity.copy()
        
        return final_control


def demo_precision_machining():
    """정밀 가공 데모"""
    print("\n" + "=" * 70)
    print("정밀 가공 시나리오: 5축 CNC 머신")
    print("=" * 70)
    print("목표: 0.00001mm 단위 정밀도로 가공")
    print("=" * 70)
    
    # 제어기 생성
    controller = PrecisionMachiningController()
    
    # 가공 궤적 정의
    target_trajectory = [
        np.array([10.0, 5.0, 2.0, 0.0, 0.0]),
        np.array([10.00001, 5.00001, 2.0, 0.0, 0.0]),  # 0.00001mm 이동
        np.array([10.00002, 5.00002, 2.0, 0.0, 0.0]),
    ]
    
    # 맥락 정보 (도구, 온도)
    context = {
        'tool': 'diamond',
        'temperature': 25.0,
        'material': 'titanium'
    }
    
    print("\n가공 시작:")
    print(f"{'Step':>6} | {'Target X':>12} | {'Current X':>12} | {'Error (mm)':>12} | {'Correction':>12}")
    print("-" * 70)
    
    errors = []
    corrections = []
    
    for step, target in enumerate(target_trajectory):
        # 제어 신호 계산
        control = controller.control_step(target, dt=0.001, context=context)
        
        # 오차 계산
        error = target - controller.current_position
        error_norm = np.linalg.norm(error)
        correction_norm = np.linalg.norm(control - controller.pid.compute(error, 0.001))
        
        errors.append(error_norm)
        corrections.append(correction_norm)
        
        print(f"{step+1:6d} | {target[0]:12.8f} | {controller.current_position[0]:12.8f} | "
              f"{error_norm*1000:12.6f} | {correction_norm*1000:12.6f}")
    
    print("\n" + "=" * 70)
    print("결과 분석:")
    print("=" * 70)
    print(f"평균 오차: {np.mean(errors)*1000:.6f} mm")
    print(f"최대 오차: {np.max(errors)*1000:.6f} mm")
    print(f"평균 보정: {np.mean(corrections)*1000:.6f} mm")
    print("=" * 70)
    
    if np.mean(errors) < 0.00001:  # 0.00001mm 이하
        print("✅ 정밀 가공 목표 달성!")
    else:
        print("⚠️ 추가 튜닝 필요")


def main():
    """메인 함수"""
    demo_precision_machining()
    
    print("\n" + "=" * 70)
    print("정밀 가공 시나리오 완료")
    print("=" * 70)
    print("소뇌 엔진이 정밀 가공 제어에 적용되었습니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()

