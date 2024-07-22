# Account App(사용자)

- 예약 시스템을 이용하는 고객과 관리자의 정보를 생성하고 관리하는 APP

# 기능

## 기본 사용자 생성하기

- 해당 기능은 관리자(superuser)와 일반 고객(user)를 기본적으로 생성하는 commands 입니다.
- !!!해당 기능은 `local`에서만 사용해주세요.

### local 환경

- local 환경에서는 아래와 같이 명령어를 사용하시면 됩니다.

```bash
python manage.py create_default_user --settings=config.settings.local
```

- 사용자 정보

| 권한   | 아이디   | 비밀번호          | 기업              |
|------|-------|---------------|-----------------|
| 관리자  | admin | adminpassword | X               |
| 기업고객 | user  | userpassword  | example company |

### prod 환경

- `production` 환경에서는 cli를 통해 superuser를 생성해주세요.
    ```bash
    python manage.py createsuperuser --settings=config.settings.prod`   
    ```
  
## 로그인 기능

- jwt를 통한 인증 시스템 구현

### 선정 이유

1. stateless한 인증 방식
2. 클레임 안에 권한을 넣어서 사용하면 추후 api server가 scale out이 되어도 데이터 동기화 문제가 생기지 않을 것 같다.
