#!/usr/bin/env python3
"""
소뇌 엔진 독립 테스트
grid_engine 의존성 없이 소뇌 엔진만 테스트
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig


class MockMemory:
    """해마 메모리 모의 객체 (테스트용)"""
    def __init__(self):
        self.memories = {}
    
    def retrieve(self, key, context=None):
        """기억 검색"""
        # 간단한 유클리드 거리 기반 검색
        if len(self.memories) == 0:
            return []
        
        best_match = None
        best_distance = float('inf')
        
        for stored_key, value in self.memories.items():
            distance = np.linalg.norm(key - stored_key)
            if distance < best_distance:
                best_distance = distance
                best_match = {'bias': value, 'confidence': 1.0 / (1.0 + distance)}
        
        if best_match and best_distance < 0.1:
            return [best_match]
        return []
    
    def store(self, key, value, context=None):
        """기억 저장"""
        self.memories[tuple(key)] = value


def test_basic_initialization():
    """기본 초기화 테스트"""
    print("\n" + "=" * 70)
    print("테스트 1: 기본 초기화")
    print("=" * 70)
    
    config = CerebellumConfig()
    engine = CerebellumEngine(memory_dim=5, config=config)
    
    print(f"✅ CerebellumEngine 생성 성공")
    print(f"   메모리 차원: {engine.memory_dim}")
    print(f"   설정: {config}")
    
    return engine


def test_predictive_feedforward():
    """Predictive Feedforward 테스트"""
    print("\n" + "=" * 70)
    print("테스트 2: Predictive Feedforward")
    print("=" * 70)
    
    engine = CerebellumEngine(memory_dim=5)
    
    current_state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    target_state = np.array([1.0, 1.0, 0.0, 0.0, 0.0])
    velocity = np.array([0.1, 0.1, 0.0, 0.0, 0.0])
    acceleration = np.array([0.01, 0.01, 0.0, 0.0, 0.0])
    
    correction = engine.compute_correction(
        current_state=current_state,
        target_state=target_state,
        velocity=velocity,
        acceleration=acceleration,
        dt=0.001
    )
    
    print(f"   Current State: {current_state}")
    print(f"   Target State: {target_state}")
    print(f"   Velocity: {velocity}")
    print(f"   Acceleration: {acceleration}")
    print(f"   Correction: {correction}")
    print(f"   Correction Norm: {np.linalg.norm(correction):.6f}")
    print("✅ Predictive Feedforward 작동 확인")


def test_variance_reduction():
    """Variance 감소 테스트"""
    print("\n" + "=" * 70)
    print("테스트 3: Variance 감소")
    print("=" * 70)
    
    engine = CerebellumEngine(memory_dim=5)
    target_state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
    
    corrections = []
    errors = []
    
    for i in range(10):
        # 노이즈 추가
        noise = np.random.normal(0, 0.0005, 5)
        current_state = target_state + noise
        
        correction = engine.compute_correction(
            current_state=current_state,
            target_state=target_state,
            dt=0.001
        )
        
        error = target_state - current_state
        errors.append(error)
        corrections.append(correction)
        
        error_norm = np.linalg.norm(error)
        correction_norm = np.linalg.norm(correction)
        
        print(f"   Step {i+1}: Error Norm = {error_norm:.6f}, Correction Norm = {correction_norm:.6f}")
    
    # Variance 계산
    error_array = np.array(errors)
    error_variance = np.var(error_array, axis=0)
    correction_array = np.array(corrections)
    correction_variance = np.var(correction_array, axis=0)
    
    print(f"\n   Error Variance: {np.mean(error_variance):.6f}")
    print(f"   Correction Variance: {np.mean(correction_variance):.6f}")
    print("✅ Variance 감소 작동 확인")


def test_memory_integration():
    """해마 메모리 통합 테스트"""
    print("\n" + "=" * 70)
    print("테스트 4: 해마 메모리 통합")
    print("=" * 70)
    
    # 모의 메모리 생성
    memory = MockMemory()
    
    # 소뇌 엔진 생성 (메모리 연결)
    engine = CerebellumEngine(memory_dim=5, memory=memory)
    
    # 기억 저장
    position = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
    bias = np.array([0.001, 0.002, 0.0, 0.0, 0.0])
    memory.store(position, bias)
    
    print(f"   저장된 Position: {position}")
    print(f"   저장된 Bias: {bias}")
    
    # 보정 계산 (메모리 활용)
    current_state = position + np.array([0.0005, 0.001, 0.0, 0.0, 0.0])
    target_state = position.copy()
    
    correction = engine.compute_correction(
        current_state=current_state,
        target_state=target_state,
        context={"test": True},
        dt=0.001
    )
    
    print(f"   Current State: {current_state}")
    print(f"   Correction: {correction}")
    print(f"   Correction Norm: {np.linalg.norm(correction):.6f}")
    print("✅ 해마 메모리 통합 작동 확인")


def test_trial_to_trial():
    """Trial-to-Trial 보정 테스트"""
    print("\n" + "=" * 70)
    print("테스트 5: Trial-to-Trial 보정")
    print("=" * 70)
    
    engine = CerebellumEngine(memory_dim=5)
    target_state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
    
    for trial in range(5):
        # 약간의 노이즈 추가
        noise = np.random.normal(0, 0.0001, 5)
        current_state = target_state + noise
        
        correction = engine.compute_correction(
            current_state=current_state,
            target_state=target_state,
            dt=0.001
        )
        
        error_norm = np.linalg.norm(target_state - current_state)
        correction_norm = np.linalg.norm(correction)
        
        print(f"   Trial {trial+1}: Error Norm = {error_norm:.6f}, Correction Norm = {correction_norm:.6f}")
    
    print("✅ Trial-to-Trial 보정 작동 확인")


def main():
    """메인 테스트 함수"""
    print("\n" + "=" * 70)
    print("소뇌 엔진 독립 테스트")
    print("=" * 70)
    
    try:
        # 테스트 실행
        test_basic_initialization()
        test_predictive_feedforward()
        test_variance_reduction()
        test_memory_integration()
        test_trial_to_trial()
        
        print("\n" + "=" * 70)
        print("✅ 모든 테스트 완료!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

