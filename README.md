# 예약 시스템

## 소개

기업 고객이 예약을 할 수 있는 웹 어플리케이션

## 기능 요구사항

[기능 요구사항 정리](./docs/analyzing-functional-requirements.md)

## 테이블 설계 스케치

[테이블 설계 스케치](./docs/db.md)

# 프로젝트 시작하기

## 필요한 요소 세팅 및 Django App 실행하기

- 들어가기에 앞서 `poetry`와 `docker`를 설치해주세요.
    - poetry 설치 방법: https://python-poetry.org/docs/#installation
    - docker 설치 방법: https://docs.docker.com/engine/install/

- DJANGO_SETTING_MODULE 설정하기
    - 현재 개발환경에서는 `config.settings.local`을 사용하고 있습니다.
    - 따라서 명령마다 --settings 옵션을 넣기 불편하다면 **DJANGO_SETTING_MODULE**을 `config.settings.local`로 환경변수로 설정해주세요.

## docker-compose로 로컬환경에서 예약 시스템 실행하기

- 만약 docker-compose를 통해 Django를 실행시키고 싶다면 steps를 따라주세요.

### 1. docker-compose 서비스 실행

- docker compose 를 통해 db와 test, was를 실행합니다.

  ```bash
  docker-compose up --build -d db
  docker-compose up --build -d web
  ```

- 관리자는 아래의 계정 정보를 통해 로그인 할 수 있습니다.

```markdown
- email: admin@example.com
- password: adminpassword
```

- 만약 windows 환경에서 실행이 안 된다면 os 환경에 따른 줄바꿈 문제일 수 있습니다.
- linux os의 줄바꿈 방식(LF)으로 변경해 주세요.

### 2. docker-compose 서비스 종료

- 확인했다면 docker-compose에 떠있는 container를 종료시킵니다.

  ```bash
  docker-compose down
  ```

### 3 test 실행

- 테스트를 진행 할 수 있습니다.
  ```bash
  docker-compose up --build test_web
  ```

## 환경변수

- 기본값이 없는 경우 **직접 지정해야 합니다.**

### Django Config

| 변수명                    | 기본값                      | 비고                                                      |
|------------------------|--------------------------|---------------------------------------------------------| 
| DJANGO_SETTINGS_MODULE | 없음                       |                                                         |
| SECRET_KEY             | 94n7fx27pd-...           | local 환경과 test 환경에서는 기본값을 사용하지만 <br/> prod에서는 주입해야 합니다. |
| JWT_ACCESS_LIFETIME    | 60                       | JWT ACCESS TOKEN의 유효 시간(분)                              |
| JWT_REFRESH_LIFETIME   | 24                       | JWT REFRESH TOKEN의 유효 시간(시)                             |
| JWT_SECRET_KEY         | 로컬 환경에서 local-secret-key | JWT의 SECRET KEY                                         |

### DB

| 변수명         | 기본값       |
|-------------|-----------|
| DB_NAME     | postgres  |
| DB_USER     | postgres  |
| DB_PASSWORD | postgres  |
| DB_HOST     | localhost |
| DB_PORT     | 5432      |


## 시스템 설명 방법

- 해당 시스템의 이용 방법을 시나리오를 통해 설명하고 있다
- [시나리오 보기](docs/scenario.md)
