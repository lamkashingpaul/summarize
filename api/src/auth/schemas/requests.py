from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
)


class UserRegister(BaseModel):
    email: Annotated[
        str,
        ...,
        Field(description="The email address of the user."),
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=5,
            max_length=255,
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
    ]
    password: Annotated[
        str,
        ...,
        Field(description="The password for the user account."),
    ]
    name: Annotated[
        str,
        ...,
        Field(description="The name of the user."),
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=100,
        ),
    ]
    image_url: Annotated[
        Optional[str],
        Field(description="The URL of the user's profile image."),
        StringConstraints(
            strip_whitespace=True,
            min_length=0,
            max_length=255,
        ),
    ] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
                "password": "foo@bar.com",
                "name": "John Doe",
                "image_url": "https://example.com/profile.jpg",
            }
        }
    )

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if len(value) > 128:
            raise ValueError("Password must not exceed 128 characters.")

        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter.")

        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")

        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in value):
            raise ValueError("Password must contain at least one special character.")

        return value


class VerificationEmailResend(BaseModel):
    email: Annotated[
        str,
        ...,
        Field(description="The email address of the user."),
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=5,
            max_length=255,
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
    ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
            }
        }
    )


class ResetPasswordEmailSend(BaseModel):
    email: Annotated[
        str,
        ...,
        Field(description="The email address of the user."),
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=5,
            max_length=255,
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
    ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
            }
        }
    )


class EmailVerify(BaseModel):
    token: Annotated[
        str,
        ...,
        Field(description="The verification token sent to the user's email."),
    ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
                "token": "1234567890abcdef",
            }
        }
    )


class PasswordReset(BaseModel):
    token: Annotated[
        str,
        ...,
        Field(description="The password reset token sent to the user's email."),
    ]
    new_password: Annotated[
        str,
        ...,
        Field(description="The new password for the user account."),
    ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "1234567890abcdef",
                "new_password": "new_secure_password",
            }
        }
    )


class UserLogin(BaseModel):
    email: Annotated[
        str,
        ...,
        Field(description="The email address of the user."),
        StringConstraints(
            strip_whitespace=True,
            to_lower=True,
            min_length=5,
            max_length=255,
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        ),
    ]
    password: Annotated[
        str,
        ...,
        Field(description="The password for the user account."),
    ]
    remember_me: Annotated[
        Optional[bool],
        Field(
            description="Whether to remember the user on this device.",
            default=False,
        ),
    ] = False

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
                "password": "1234567890abcdef",
                "remember_me": True,
            }
        }
    )
