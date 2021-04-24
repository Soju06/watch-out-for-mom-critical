<div align="center">
# watch-out-for-mom-critical

## What is this

웹캠 하나만 있으면 당신의 사생활을 가족들로부터 안전하게 해줍니다.

<img width="70%" src="https://user-images.githubusercontent.com/34199905/115955657-de369900-a532-11eb-8be2-b2647003cd1c.gif" />

## How it works

영상 프레임을 비교하여 모션을 감지합니다.

모션이 감지되면, Ctrl + Win + Right(윈도우 이동)을 입력합니다.

` def mom_critical()`을 수정하여 기능을 변경할 수 있습니다.

카메라 모니터링이 필요없는 경우 `--no-gui`플래그로 백그라운드에서 작업할 수 있습니다.

## Getting started

* 시작하기 전에

  Python 3.7로 작성되었습니다.

  다음은 사용된 라이브러리입니다.

  ```
  numpy==1.19.5
  opencv-python==4.5.1.48
  ```

* 저장소 복제하기

  ```shell
  git clone https://github.com/Soju06/watch-out-for-mom-critical.git
  cd watch-out-for-mom-critical
  ```

* 종속성 설치하기

  ```shell
  pip install -r requirements.txt
  ```

* 실행 파라미터

  모든 파라미터는 기본값이 지정되어있어, `py main.py`로 바로 실행할 수 있습니다.

  ```python
  --sensitivity 80 # 색상 변화 민감도 백분율 0 ~ 100
  
  --max-diff 100 # 변경 사항 max-diff보다 높다면 모션을 감지합니다. 낮을수록 변화에 대해 민감해집니다.
  
  --mom-critical-ready-delay 5 # 엄크가 발생한 경우 mom-critical-ready-delay 초 후 Ready 상태로 돌아갑니다.
  
  --abs-delay-frame-count 4 # 비교할 프레임입니다. frame-count보다 높을 수 없습니다. 높을수록 움직임에 대해 민감해집니다.
  
  --frame-count 5 # 임시 프레임 개수입니다.
  
  --video 0 # 모션을 감지할 카메라 번호입니다. 카메라가 여러 개일 경우 이 값을 조정하여 설정합니다.
  
  --no-gui # 카메라 모니터링이 필요 없는 경우 이 플래그를 사용하십시오.
  ```

* 실행

  Windows인 경우

  ```
  py main.py
  ```

  Linux인 경우

  ```
  python3 main.py
  ```

  - no-gui flag

  Windows인 경우

  ```
  py main.py --no-gui
  ```

  Linux인 경우

  ```
  python3 main.py --no-gui
  ```

## Feature preview

모션 감지

![img](https://media.discordapp.net/attachments/810047161664143383/835435755512791050/wa.png)

</div>
