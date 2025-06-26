from pydantic import BaseModel, ConfigDict

from src.users.schemas.response import UserResponse


class RegisterUserResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "User registered successfully.",
            }
        }
    )


class ResendVerificationEmailResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Verification email resent successfully.",
            }
        }
    )


class SendResetPasswordEmailResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Reset password email sent successfully.",
            }
        }
    )


class VerifyEmailResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Email verification successful.",
            }
        }
    )


class ResetPasswordResponse(BaseModel):
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Password reset successful.",
            }
        }
    )


class UserLoginResponse(UserResponse, BaseModel):
    pass
