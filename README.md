## 얼굴인식 도어락 & QR 리더기 

Raspberry Pi와 Python OpenCV를 활용한 얼굴인식 도어락 및 QR 코드 기반의 스마트 도어락 시스템 구현 프로젝트입니다.

### 프로젝트 소개
이 프로젝트는 기존의 물리적 키나 단순 비밀번호 방식의 도어락을 대체하기 위해 고안된 스마트 접근 제어 시스템입니다. <br>
Raspberry Pi를 엣지 디바이스로 활용하여 카메라를 통해 출입자를 인식합니다. <br>
딥러닝 기반의 고성능 얼굴 인식 모델인 ArcFace를 사용하여 등록된 사용자를 식별하며, 사진이나 동영상을 이용한 스푸핑 공격을 방지하기 위해 눈깜빡임 기반의 생체인증미션을 수행해야 문이 열립니다. <br>
추후 물건에 픽업 수단으로 QR 코드 인증도 지원합니다.

### 주요 기능
고성능 얼굴 인식: ArcFace를 활용하여 높은 정확도의 얼굴 식별을 제공합니다.

강력한 보안 : 단순 얼굴 일치뿐만 아니라, 실시간 눈깜빡임 미션(예: "3초 안에 눈을 2번 깜빡이세요")을 통과해야만 실제 사람으로 간주하여, 사진/동영상 도용을 원천 차단합니다.

### 유스케이스
사용자가 시스템을 이용하는 전체적인 흐름입니다.<br><br>
<img width="600" height="400" alt="스크린샷 2025-09-12 164813" src="https://github.com/user-attachments/assets/ae489397-e1ee-42d4-a5db-938e8056787c" />


### 시스템 아키텍처
얼굴인식 도어락과 QR 리더기 아키텍처입니다.<br><br>
<img width="500" height="430" alt="DoorLock(Face-ID)" src="https://github.com/user-attachments/assets/0082ca65-bb15-497b-be66-7cfd909eed47" />
<img width="500" height="373" alt="QR Reader" src="https://github.com/user-attachments/assets/8e0d33b6-1c44-4868-9a14-aa363dc8c33e" />


작동 메커니즘 상세
얼굴 감지 및 전송: 라즈베리파이 카메라가 접근자를 감지하면 얼굴 영역을 크롭하여 서버로 전송합니다.

벡터 추출 및 비교 : 서버는 전송받은 얼굴 이미지에서 ArcFace를 이용해 특징 벡터를 추출하고, DB에 사전 등록된 사용자의 벡터와 코사인 유사도를 비교.

생체인증 미션 시작 : 서버에서 벡터가 일치한다는 응답이 오면, 라즈베리파이는 즉시 문을 열지 않고 생체인증 미션(눈깜빡임 N회) 모드로 진입.

미션 수행 및 검증: OpenCV를 통해 실시간으로 눈의 깜빡임 여부를 판단합니다. 정해진 시간 내에 할당된 횟수만큼 깜빡임이 감지되면 미션 성공으로 간주.

도어 개방: 미션 성공 시 GPIO 신호를 보내 솔레노이드 락 또는 릴레이를 작동시켜 문을 엽니다.

### 기술 스택
#### H/W <br>
Raspberry Pi 4 Model B (or higher)

Pi Camera Module v2

Solenoid Lock & Relay module

#### S/W & Libraries
Language: Python 

Vision: OpenCV 

Face Recognition Model: DeepFace (Model: ArcFace)

QR Reading: opencv-python built-in QR detector

Communication: REST API Requests

### 결과 영상 
