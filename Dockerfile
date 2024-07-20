# 첫 번째 단계: 의존성 설치
FROM python:3.11-alpine as builder

WORKDIR /mysite

# poetry 설치
RUN pip install poetry

# 프로젝트 의존성 복사 및 설치
COPY pyproject.toml poetry.lock /mysite/
RUN poetry export -f requirements.txt --output requirements.txt --with dev
RUN poetry export -f requirements.txt --output requirements_test.txt --with test


# 두 번째 단계: 테스트 실행
FROM python:3.11-alpine as test

WORKDIR /mysite

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings.test
# 의존성 설치
COPY --from=builder /mysite/requirements_test.txt /mysite/
RUN pip install -r requirements_test.txt

# 프로젝트 코드 복사
COPY . /mysite

RUN chmod +x /mysite/entrypoint.sh
ENTRYPOINT ["/mysite/entrypoint.sh"]

# 세 번째 단계: 빌드
FROM python:3.11-alpine as deploy

WORKDIR /mysite

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# 의존성 설치
COPY --from=builder /mysite/requirements.txt /mysite/
RUN pip install -r requirements.txt

# 프로젝트 코드 복사
COPY . /mysite

EXPOSE 8000

# entrypoint.sh 파일 실행
RUN chmod +x /mysite/entrypoint.sh
ENTRYPOINT ["/mysite/entrypoint.sh"]