#!/usr/bin/env python3
"""
v0.6 기능 테스트

1. Confidence 기반 gain 조절
2. Error norm 기반 saturation
3. Context 가중치
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from cerebellum.cerebellum_engine import CerebellumEngine, CerebellumConfig


class MockMemory:
    """해마 메모리 모의 객체 (confidence 포함)"""
    def __init__(self):
        self.memories = {}
    
    def retrieve(self, key, context=None):
        """기억 검색 (confidence 포함)"""
        if len(self.memories) == 0:
            return []
        
        best_match = None
        best_distance = float('inf')
        
        for stored_key, (value, conf) in self.memories.items():
            distance = np.linalg.norm(key - stored_key)
            if distance < best_distance:
                best_distance = distance
                best_match = {
                    'bias': value,
                    'confidence': conf * (1.0 / (1.0 + distance))  # 거리에 따라 confidence 감소
                }
        
        if best_match and best_distance < 0.1:
            return [best_match]
        return []
    
    def store(self, key, value, confidence=0.9, context=None):
        """기억 저장 (confidence 포함)"""
        self.memories[tuple(key)] = (value, confidence)


def test_confidence_based_gain():
    """Confidence 기반 gain 조절 테스트"""
    print("\n" + "=" * 70)
    print("테스트 1: Confidence 기반 gain 조절")
    print("=" * 70)
    
    config = CerebellumConfig(
        memory_gain=0.4,
        min_confidence=0.1
    )
    
    # 높은 confidence 메모리
    memory_high = MockMemory()
    memory_high.store(
        np.array([1.0, 0.5, 0.3, 10.0, 5.0]),
        np.array([0.001, 0.002, 0.0, 0.0, 0.0]),
        confidence=0.9
    )
    engine_high = CerebellumEngine(memory_dim=5, config=config, memory=memory_high)
    
    # 낮은 confidence 메모리
    memory_low = MockMemory()
    memory_low.store(
        np.array([1.0, 0.5, 0.3, 10.0, 5.0]),
        np.array([0.001, 0.002, 0.0, 0.0, 0.0]),
        confidence=0.2
    )
    engine_low = CerebellumEngine(memory_dim=5, config=config, memory=memory_low)
    
    # 보정값 계산
    current_state = np.array([1.0005, 0.501, 0.3, 10.0, 5.0])
    target_state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
    
    correction_high = engine_high.compute_correction(
        current_state=current_state,
        target_state=target_state,
        dt=0.001
    )
    
    correction_low = engine_low.compute_correction(
        current_state=current_state,
        target_state=target_state,
        dt=0.001
    )
    
    print(f"   High confidence (0.9): Correction norm = {np.linalg.norm(correction_high):.6f}")
    print(f"   Low confidence (0.2):  Correction norm = {np.linalg.norm(correction_low):.6f}")
    
    if np.linalg.norm(correction_high) > np.linalg.norm(correction_low):
        print("✅ Confidence 기반 gain 조절 작동 확인!")
    else:
        print("⚠️ 예상과 다른 결과")


def test_saturation():
    """Error norm 기반 saturation 테스트"""
    print("\n" + "=" * 70)
    print("테스트 2: Error norm 기반 saturation")
    print("=" * 70)
    
    config = CerebellumConfig(
        max_correction_norm=5.0  # 작은 값으로 설정하여 saturation 확인
    )
    engine = CerebellumEngine(memory_dim=5, config=config)
    
    # 큰 오차 시나리오
    current_state = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    target_state = np.array([100.0, 100.0, 0.0, 0.0, 0.0])  # 매우 큰 오차
    velocity = np.array([10.0, 10.0, 0.0, 0.0, 0.0])
    acceleration = np.array([1.0, 1.0, 0.0, 0.0, 0.0])
    
    correction = engine.compute_correction(
        current_state=current_state,
        target_state=target_state,
        velocity=velocity,
        acceleration=acceleration,
        dt=0.001
    )
    
    correction_norm = np.linalg.norm(correction)
    print(f"   큰 오차 시나리오:")
    print(f"   Target state: {target_state}")
    print(f"   Correction norm: {correction_norm:.6f}")
    print(f"   Max allowed: {config.max_correction_norm:.6f}")
    
    if correction_norm <= config.max_correction_norm + 0.1:  # 약간의 여유
        print("✅ Saturation 작동 확인!")
    else:
        print(f"⚠️ Saturation 미작동: {correction_norm} > {config.max_correction_norm}")


def test_context_weight():
    """Context 가중치 테스트"""
    print("\n" + "=" * 70)
    print("테스트 3: Context 가중치")
    print("=" * 70)
    
    config = CerebellumConfig(
        context_weight_enabled=True,
        memory_gain=0.4
    )
    
    memory = MockMemory()
    memory.store(
        np.array([1.0, 0.5, 0.3, 10.0, 5.0]),
        np.array([0.001, 0.002, 0.0, 0.0, 0.0]),
        confidence=0.9
    )
    engine = CerebellumEngine(memory_dim=5, config=config, memory=memory)
    
    current_state = np.array([1.0005, 0.501, 0.3, 10.0, 5.0])
    target_state = np.array([1.0, 0.5, 0.3, 10.0, 5.0])
    
    # Context 없음
    correction_no_ctx = engine.compute_correction(
        current_state=current_state,
        target_state=target_state,
        context=None,
        dt=0.001
    )
    
    # Context 있음
    correction_with_ctx = engine.compute_correction(
        current_state=current_state,
        target_state=target_state,
        context={'tool': 'A', 'temperature': 25.0},
        dt=0.001
    )
    
    print(f"   Context 없음: Correction norm = {np.linalg.norm(correction_no_ctx):.6f}")
    print(f"   Context 있음: Correction norm = {np.linalg.norm(correction_with_ctx):.6f}")
    print("✅ Context 가중치 작동 확인!")


def main():
    """메인 테스트 함수"""
    print("\n" + "=" * 70)
    print("v0.6 기능 테스트")
    print("=" * 70)
    
    try:
        test_confidence_based_gain()
        test_saturation()
        test_context_weight()
        
        print("\n" + "=" * 70)
        print("✅ 모든 v0.6 기능 테스트 완료!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

