from dataclasses import dataclass


@dataclass
class AccountSignUpResponse:
    DUPLICATE_EMAIL = "이미 존재하는 이메일입니다."
