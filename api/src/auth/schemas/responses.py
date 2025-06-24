from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    email: str
    name: str
    image_url: str | None = None
    is_email_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
                "name": "Foo Bar",
                "image_url": "https://example.com/image.jpg",
                "is_email_verified": True,
            }
        },
    )


class RegisterUserResponse(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "User registered successfully.",
            }
        }
    )


class VerifyEmailResponse(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Email verification successful.",
            }
        }
    )


class ResendVerificationEmailResponse(BaseModel):
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Verification email resent successfully.",
            }
        }
    )


class UserLoginResponse(UserResponse, BaseModel):
    pass
