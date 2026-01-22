#!/bin/bash
# 깃허브 업로드 명령어 스크립트

echo "=== 소뇌 엔진 깃허브 업로드 ==="
echo ""

# 현재 상태 확인
echo "1. 현재 Git 상태 확인:"
git status --short | head -10
echo ""

# 브랜치 확인
echo "2. 현재 브랜치:"
git branch
echo ""

# 원격 저장소 확인
echo "3. 원격 저장소:"
git remote -v
echo ""

echo "=== 업로드 명령어 ==="
echo ""
echo "# 1. GitHub에서 저장소 생성 후:"
echo "git remote add origin https://github.com/YOUR_USERNAME/cerebellum-engine.git"
echo ""
echo "# 2. 브랜치 이름 변경 (필요시):"
echo "git branch -M main"
echo ""
echo "# 3. 업로드:"
echo "git push -u origin main"
echo ""
echo "=== 완료 ==="
