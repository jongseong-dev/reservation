from drf_spectacular.utils import OpenApiExample


account_sign_up_examples = [
    OpenApiExample(
        "유효한 가입 양식",
        summary="유효한 가입 양식",
        description="username과 password 중복되지 않은 email을 통해 가입합니다.",
        value={
            "username": "이종성",
            "email": "test.user@exmaple.com",
            "password": "password",
        },
        request_only=True,
        status_codes=["200"],
    ),
    OpenApiExample(
        "중복된 이메일로 유효하지 않은 가입",
        summary="유효하지 않은 가입 양식",
        description="중복된 이메일로 가입합니다.",
        value={
            "username": "이종성",
            "email": "user@exmaple.com",
            "password": "password",
        },
        request_only=True,
        status_codes=["400"],
    ),
]
