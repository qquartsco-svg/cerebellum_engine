# GitHub 인증 가이드

## 디바이스 인증 코드 받기

### 방법 1: GitHub CLI 사용 (가장 쉬움)

```bash
gh auth login --device
```

이 명령어를 실행하면:
1. 터미널에 코드가 표시됩니다
2. 브라우저가 자동으로 열립니다
3. 표시된 코드를 브라우저에 입력하세요

### 방법 2: 수동 인증

1. 브라우저에서 https://github.com/login/device 접속
2. 터미널에서 `gh auth login --device` 실행
3. 표시된 코드를 브라우저에 입력

### 방법 3: GitHub CLI 설치 (없는 경우)

```bash
# macOS
brew install gh

# 또는 공식 사이트에서 다운로드
# https://cli.github.com/
```

## 인증 확인

```bash
gh auth status
```

## 저장소 업로드

인증 후:

```bash
cd /Users/jazzin/Desktop/00_BRAIN/5.Cerebellum_Engine

# 원격 저장소 추가
git remote add origin https://github.com/YOUR_USERNAME/cerebellum-engine.git

# 업로드
git push -u origin main
```

---

**참고**: GitHub CLI를 사용하면 더 쉽게 인증할 수 있습니다.

