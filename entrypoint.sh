#!/bin/sh

# DJANGO_SETTINGS_MODULE 환경변수가 설정되어 있지 않다면 기본값으로 config.settings.local을 사용합니다.
if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
  export DJANGO_SETTINGS_MODULE=config.settings.local
fi

cd webapp
# Django 애플리케이션을 실행합니다.
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.local" ]; then
  python manage.py migrate
  python manage.py create_default_user  # 관리자와 일반 사용자를 기본으로 추가함 local 환경에서만 추가
  python manage.py runserver 0.0.0.0:8000
elif [ "$DJANGO_SETTINGS_MODULE" = "config.settings.test" ]; then
  pytest
elif [ "$DJANGO_SETTINGS_MODULE" = "config.settings.prod" ]; then
  python manage.py migrate
  python manage.py collectstatic
  gunicorn --bind 0:8000 webapp.wsgi:application
fi