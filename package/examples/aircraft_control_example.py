#!/usr/bin/env python3
"""
항공기 제어 시나리오 예시

자동 조종 시스템에서 소뇌 엔진을 사용한 공기역학적 지연 보정

Author: GNJz
Created: 2026-01-22
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig


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


class AircraftController:
    """항공기 제어기 (소뇌 엔진 사용)"""
    
    def __init__(self):
        # 해마 메모리
        self.memory = MockMemory()
        
        # 소뇌 엔진 (공기역학적 지연 보정용)
        config = CerebellumConfig(
            feedforward_gain=0.6,  # 높은 gain (예측 중요)
            prediction_horizon=0.05,  # 50ms 예측 (공기역학적 지연)
            trial_gain=0.3,
            variance_gain=0.2,
            memory_gain=0.4,
            max_correction_norm=2.0
        )
        self.cerebellum = CerebellumEngine(memory_dim=3, config=config, memory=self.memory)
        
        # 상태 추적 (자세: [roll, pitch, yaw])
        self.current_attitude = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0, 0.0])
    
    def control_step(self, target_attitude, altitude=10000.0, airspeed=250.0, dt=0.01):
        """
        한 스텝 제어
        
        Args:
            target_attitude: 목표 자세 [roll, pitch, yaw] (라디안)
            altitude: 고도 (feet)
            airspeed: 속도 (knots)
            dt: 시간 간격 (초)
        
        Returns:
            control_signal: 제어 신호
        """
        # 오차 계산
        error = target_attitude - self.current_attitude
        
        # 소뇌 보정 (공기역학적 지연 보정)
        cerebellum_correction = self.cerebellum.compute_correction(
            current_state=self.current_attitude,
            target_state=target_attitude,
            velocity=self.velocity,
            acceleration=self.acceleration,
            context={'altitude': altitude, 'airspeed': airspeed, 'mode': 'autopilot'},
            dt=dt
        )
        
        # 최종 제어 신호 (소뇌 보정만 사용 - 자동 조종 시스템)
        final_control = cerebellum_correction
        
        # 상태 업데이트 (시뮬레이션)
        self.current_attitude += final_control * dt
        self.velocity = (self.current_attitude - self.prev_attitude) / dt if hasattr(self, 'prev_attitude') else np.zeros(3)
        self.acceleration = (self.velocity - self.prev_velocity) / dt if hasattr(self, 'prev_velocity') else np.zeros(3)
        
        self.prev_attitude = self.current_attitude.copy()
        self.prev_velocity = self.velocity.copy()
        
        # 안정 구간에서 기억 저장
        if np.linalg.norm(error) < 0.01:
            self.memory.store(
                key=self.current_attitude,
                value=error,
                confidence=0.9 - np.linalg.norm(error) * 10,
                context={'altitude': altitude, 'airspeed': airspeed}
            )
        
        return final_control


def demo_aircraft_control():
    """항공기 제어 데모"""
    print("\n" + "=" * 70)
    print("항공기 제어 시나리오: 자동 조종 시스템")
    print("=" * 70)
    print("목표: 공기역학적 지연 보정 및 안정적인 자세 유지")
    print("=" * 70)
    
    # 제어기 생성
    controller = AircraftController()
    
    # 자세 변경 시나리오 (상승 → 수평 → 하강)
    target_attitudes = [
        np.array([0.0, 0.0, 0.0]),      # 수평
        np.array([0.0, 0.1, 0.0]),     # 상승 (pitch up)
        np.array([0.0, 0.1, 0.0]),     # 유지
        np.array([0.0, 0.0, 0.0]),     # 수평 복귀
        np.array([0.0, -0.1, 0.0]),    # 하강 (pitch down)
        np.array([0.0, 0.0, 0.0]),     # 수평 복귀
    ]
    
    print(f"\n자세 변경 시작: {len(target_attitudes)}개 단계")
    print(f"{'Step':>6} | {'Target Pitch':>15} | {'Current Pitch':>15} | {'Error':>12} | {'Correction':>12}")
    print("-" * 70)
    
    errors = []
    corrections = []
    
    step = 0
    for target in target_attitudes:
        for _ in range(100):  # 각 단계당 100 스텝
            control = controller.control_step(
                target_attitude=target,
                altitude=10000.0,
                airspeed=250.0,
                dt=0.01
            )
            
            error = target - controller.current_attitude
            error_norm = np.linalg.norm(error)
            correction_norm = np.linalg.norm(control)
            
            errors.append(error_norm)
            corrections.append(correction_norm)
            
            step += 1
            if step % 50 == 0:
                print(f"{step:6d} | {target[1]:15.6f} | {controller.current_attitude[1]:15.6f} | "
                      f"{error_norm:12.6f} | {correction_norm:12.6f}")
    
    print("\n" + "=" * 70)
    print("결과 분석:")
    print("=" * 70)
    print(f"평균 오차: {np.mean(errors):.6f} rad")
    print(f"최대 오차: {np.max(errors):.6f} rad")
    print(f"평균 보정: {np.mean(corrections):.6f} rad")
    print(f"저장된 기억 수: {len(controller.memory.memories)}")
    print("=" * 70)
    
    if np.mean(errors) < 0.01:
        print("✅ 항공기 제어 목표 달성!")
    else:
        print("⚠️ 추가 튜닝 필요")


def main():
    """메인 함수"""
    demo_aircraft_control()
    
    print("\n" + "=" * 70)
    print("항공기 제어 시나리오 완료")
    print("=" * 70)
    print("소뇌 엔진이 항공기 제어에 적용되었습니다.")
    print("=" * 70)


if __name__ == "__main__":
    main()

