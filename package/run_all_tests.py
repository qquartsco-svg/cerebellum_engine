#!/usr/bin/env python3
"""
전체 테스트 실행 스크립트

모든 테스트를 순차적으로 실행하고 결과를 요약합니다.

Author: GNJz
Created: 2026-01-22
"""

import sys
import os
import subprocess
from pathlib import Path

def run_test(test_file, description):
    """테스트 실행"""
    print(f"\n{'='*70}")
    print(f"테스트: {description}")
    print(f"파일: {test_file}")
    print(f"{'='*70}")
    
    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    if result.returncode == 0:
        print("✅ 통과")
        return True
    else:
        print("❌ 실패")
        print(result.stderr)
        return False

def main():
    """메인 함수"""
    print("\n" + "="*70)
    print("소뇌 엔진 전체 테스트")
    print("="*70)
    
    tests = [
        ("test_cerebellum_standalone.py", "독립 테스트"),
        ("test_v0.6_features.py", "v0.6 기능 테스트"),
    ]
    
    results = []
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((test_file, description, success))
    
    # 결과 요약
    print("\n" + "="*70)
    print("테스트 결과 요약")
    print("="*70)
    
    passed = sum(1 for _, _, success in results if success)
    total = len(results)
    
    for test_file, description, success in results:
        status = "✅ 통과" if success else "❌ 실패"
        print(f"{status} - {description} ({test_file})")
    
    print(f"\n총 {total}개 테스트 중 {passed}개 통과")
    
    if passed == total:
        print("\n✅ 모든 테스트 통과!")
        return 0
    else:
        print(f"\n⚠️ {total - passed}개 테스트 실패")
        return 1

if __name__ == "__main__":
    exit(main())

