#!/usr/bin/env python3
"""
로봇 팔 제어 시나리오 예시

산업용 로봇 팔에서 소뇌 엔진을 사용한 궤적 추적 제어

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
        self.integral = np.zeros(6)  # 6축 로봇 팔
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


class MockMemory:
    """해마 메모리 모의 객체"""
    def __init__(self):
        self.memories = {}
    
    def retrieve(self, key, context=None):
        """기억 검색"""
        if len(self.memories) == 0:
            return []
        
        best_match = None
        best_distance = float('inf')
        
        for stored_key, (value, conf) in self.memories.items():
            distance = np.linalg.norm(key - np.array(stored_key))
            if distance < best_distance:
                best_distance = distance
                adjusted_confidence = conf * (1.0 / (1.0 + distance))
                best_match = {
                    'bias': value,
                    'confidence': adjusted_confidence
                }
        
        if best_match and best_distance < 0.1:
            return [best_match]
        return []
    
    def store(self, key, value, confidence=0.9, context=None):
        """기억 저장"""
        self.memories[tuple(key)] = (value, confidence)


class RobotArmController:
    """로봇 팔 제어기 (PID + Cerebellum)"""
    
    def __init__(self):
        # PID 제어기
        self.pid = SimplePID(kp=1.0, ki=0.1, kd=0.05)
        
        # 해마 메모리
        self.memory = MockMemory()
        
        # 소뇌 엔진
        config = CerebellumConfig(
            feedforward_gain=0.5,
            trial_gain=0.3,
            variance_gain=0.2,
            memory_gain=0.4,
            max_correction_norm=5.0
        )
        self.cerebellum = CerebellumEngine(memory_dim=6, config=config, memory=self.memory)
        
        # 상태 추적 (6축 로봇 팔: [x, y, z, roll, pitch, yaw])
        self.current_joints = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    
    def control_step(self, target_joints, payload_weight=0.0, dt=0.001):
        """
        한 스텝 제어
        
        Args:
            target_joints: 목표 관절 각도 [x, y, z, roll, pitch, yaw]
            payload_weight: 페이로드 무게 (kg)
            dt: 시간 간격
        
        Returns:
            control_signal: 제어 신호
        """
        # 오차 계산
        error = target_joints - self.current_joints
        
        # 1. PID 제어 (기본 제어)
        pid_output = self.pid.compute(error, dt)
        
        # 2. 소뇌 보정 (정밀 보정)
        cerebellum_correction = self.cerebellum.compute_correction(
            current_state=self.current_joints,
            target_state=target_joints,
            velocity=self.velocity,
            acceleration=self.acceleration,
            context={'payload': payload_weight, 'mode': 'robot_arm'},
            dt=dt
        )
        
        # 3. 최종 제어 신호 (PID + Cerebellum)
        final_control = pid_output + cerebellum_correction
        
        # 상태 업데이트 (시뮬레이션)
        self.current_joints += final_control * dt
        self.velocity = (self.current_joints - self.prev_joints) / dt if hasattr(self, 'prev_joints') else np.zeros(6)
        self.acceleration = (self.velocity - self.prev_velocity) / dt if hasattr(self, 'prev_velocity') else np.zeros(6)
        
        self.prev_joints = self.current_joints.copy()
        self.prev_velocity = self.velocity.copy()
        
        # 안정 구간에서 기억 저장
        if np.linalg.norm(error) < 0.01:
            self.memory.store(
                key=self.current_joints,
                value=error,
                confidence=0.9 - np.linalg.norm(error) * 10,
                context={'payload': payload_weight}
            )
        
        return final_control


def demo_robot_arm():
    """로봇 팔 제어 데모"""
    print("\n" + "=" * 70)
    print("로봇 팔 제어 시나리오: 6축 산업용 로봇 팔")
    print("=" * 70)
    print("목표: 정확한 궤적 추적 및 떨림 제거")
    print("=" * 70)
    
    # 제어기 생성
    controller = RobotArmController()
    
    # 궤적 정의 (원형 궤적)
    n_points = 50
    radius = 0.1
    center = np.array([0.5, 0.5, 0.3, 0.0, 0.0, 0.0])
    
    trajectory = []
    for i in range(n_points):
        angle = 2 * np.pi * i / n_points
        point = center.copy()
        point[0] += radius * np.cos(angle)
        point[1] += radius * np.sin(angle)
        trajectory.append(point)
    
    print(f"\n궤적 추적 시작: {n_points}개 포인트")
    print(f"{'Step':>6} | {'Error Norm':>12} | {'Correction Norm':>15} | {'Position X':>12}")
    print("-" * 70)
    
    errors = []
    corrections = []
    
    for step, target in enumerate(trajectory):
        # 제어 신호 계산
        control = controller.control_step(target, payload_weight=1.0, dt=0.001)
        
        # 오차 계산
        error = target - controller.current_joints
        error_norm = np.linalg.norm(error)
        correction_norm = np.linalg.norm(control - controller.pid.compute(error, 0.001))
        
        errors.append(error_norm)
        corrections.append(correction_norm)
        
        if (step + 1) % 10 == 0:
            print(f"{step+1:6d} | {error_norm:12.6f} | {correction_norm:15.6f} | {controller.current_joints[0]:12.6f}")
    
    print("\n" + "=" * 70)
    print("결과 분석:")
    print("=" * 70)
    print(f"평균 오차: {np.mean(errors):.6f}")
    print(f"최대 오차: {np.max(errors):.6f}")
    print(f"평균 보정: {np.mean(corrections):.6f}")
    print(f"저장된 기억 수: {len(controller.memory.memories)}")
    print("=" * 70)
    
    if np.mean(errors) < 0.01:
        print("✅ 로봇 팔 제어 목표 달성!")
    else:
        print("⚠️ 추가 튜닝 필요")


def main():
    """메인 함수"""
    demo_robot_arm()
    
    print("\n" + "=" * 70)
    print("로봇 팔 제어 시나리오 완료")
    print("=" * 70)
    print("소뇌 엔진이 로봇 팔 제어에 적용되었습니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()

