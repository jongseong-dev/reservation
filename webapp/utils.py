import os

from django.core.management import BaseCommand


def is_deployment_env() -> bool:
    """
    개발환경을 체크하는 함수

    로컬 환경이나 테스트 환경이 아닌 경우 True를 반환한다.
    return
    """
    env = os.environ.get("DJANGO_SETTINGS_MODULE", "")
    is_local_env = "local" in env
    is_test_env = "test" in env
    return not (is_local_env or is_test_env)


def stdout_error_message(self: BaseCommand, error_message: str = None):
    """
    에러 메시지를 출력하고 프로그램을 종료한다.
    """
    if error_message is None:
        error_message = "This command can only be run in local environment"
    self.stdout.write(self.style.ERROR(error_message))
    raise SystemExit
