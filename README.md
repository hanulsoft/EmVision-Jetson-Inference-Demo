# EmVision Jetson-Inference Application

EmVision에서 [Jetson Inference](https://github.com/dusty-nv/jetson-inference/tree/master)의 데모 애플리케이션을 실행하는 GUI응용프로그램 및 예제

## 소개

EmVision의 데모 GUI 애플리케이션입니다.

## 주요 기능

GUI의 해당 버튼을 클릭하면 Jetson Inference의 파이프라인이 동작합니다.

- **actionnet** : 행동 분류 모델
- **backgroundnet** : 배경 제거 모델
- **depthnet** : 깊이 인식 모델
- **detectnet** : 객체 탐지 모델
- **imagenet** : 이미지 분류 모델
- **posenet** : 포즈 인식 모델
- **segnet** : 시맨틱 세그멘테이션 모델

## 시작하기

이 섹션에서는 프로젝트를 시작하는 방법에 대한 지침을 제공합니다.

### 필요 조건

- EmVision 및 Jetson Orin 보드
- 최신 JetPack SDK
- Python 3.x
- PyQt5

### 설치 방법

먼저 [Jetson Inference의 설치지침](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md)에 따라 Jetson Inference를 설치합니다.

```bash
sudo apt update
sudo apt install -y python3-pip python3-pyqt5 git
python3 -m pip install --upgrade pip

git clone https://github.com/hanulsoft/EmVision-Jetson-Inference-Demo
cd EmVision-Jetson-Inference-Demo
pip install -r requirements.txt

# 모델 사전 다운로드 및 직렬화
python3 utils/install_models.py
```

### 사용 방법

1. 애플리케이션 실행: `python main.py`
2. 카메라의 커버를 제거합니다.
3. 버튼을 클릭하여 모델을 실행합니다.

## 기여하기

이 프로젝트는 오픈 소스이며, 커뮤니티의 기여를 환영합니다.

## 라이선스

이 프로젝트는 GNU GENERAL PUBLIC LICENSE Version 3 라이선스 하에 배포됩니다. 자세한 내용은 [`LICENSE`](./LICENSE) 파일을 참조하세요.
