# 🚌driver-monitoring-system
> #### 『AI융합 문제발굴 산학연계 해커톤』에 참가하여 제작한 결과물을 기록했습니다.

<br>

## ✨소개
- #### 주제: AI 대중교통 안전운전을 위한 운전자 모니터링 시스템
- #### 실시간으로 운전자의 이상행동을 탐지하여 음성 경고 및 관리 서비스를 제작함

<br>

## 🕒개발 기간
- 23.08.21 ~ 23.08.23 (40시간)

<br>

## 🙋‍♂️팀 구성
- ### 모델 개발
  류진혁(컴퓨터공학과 22): 모델 개발 및 학습
  
  김단호(인공지능응용학과 22): 모델 결과 후처리
  
- ### 서비스 개발
  손은결(인공지능응용학과 23): 음성 경고 서비스 구현
  
  강준(인공지능응용학과 23): 관리자 서비스 구현

<br>

## 🎯목표
- ### 1차 목표
  졸음 운전 감지 모델 제작 및 이벤트 발생 구간 영상 저장
  
  저장된 이벤트 서비스 시각화
  
- ### 2차 목표
  다중 이벤트(휴대폰 사용, 안전벨트 미착용, 핸들 손 놓음) 감지 모델 제작
  
  이벤트 발생 장면 저장 및 이벤트 식별

<br>

## 📌주요 기능
### 1. 졸음 운전 감지 모델 - [상세설명](https://github.com/RyuJinHyeok/driver-monitoring-system/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5(%EC%A1%B8%EC%9D%8C-%EA%B0%90%EC%A7%80-%EB%AA%A8%EB%8D%B8))
- 데이터 증강(데이터 편향)
- YOLOv8 기반 분류
- EAR 알고리즘
  
### 2. 다중 이벤트 감지 모델 - [상세설명](https://github.com/RyuJinHyeok/driver-monitoring-system/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5(%EB%8B%A4%EC%A4%91-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EA%B0%90%EC%A7%80-%EB%AA%A8%EB%8D%B8))
- 데이터 증강(데이터 불균형)
- YOLOv8 기반 분류
  
### 3. 이벤트 구간 탐지 및 저장 - [상세설명](https://github.com/RyuJinHyeok/driver-monitoring-system/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5(%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EA%B5%AC%EA%B0%84-%ED%83%90%EC%A7%80-%EB%B0%8F-%EC%A0%80%EC%9E%A5))
- 상태 변화 탐지
- 실시간 영상 저장(multi thread)
  
### 4. 음성 경고 - [상세설명](https://github.com/RyuJinHyeok/driver-monitoring-system/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5(%EC%9D%8C%EC%84%B1-%EA%B2%BD%EA%B3%A0))
- 실시간 음성 경고
  
### 5. 관리자 시스템 - [상세설명](https://github.com/RyuJinHyeok/driver-monitoring-system/wiki/%EC%A3%BC%EC%9A%94-%EA%B8%B0%EB%8A%A5(%EA%B4%80%EB%A6%AC%EC%9E%90-%EC%8B%9C%EC%8A%A4%ED%85%9C))
- 분류 기능(id, event별)
