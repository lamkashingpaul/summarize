from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, BackgroundTasks, Header, Request, Response

from src.auth.dependencies import OptionalSessionUser
from src.auth.models.session import Session
from src.auth.models.verification import VerificationIdentifier, VerificationType
from src.auth.schemas.internals import CreateSessionDto, CreateVerificationDto
from src.auth.schemas.requests import (
    EmailVerify,
    PasswordReset,
    ResetPasswordEmailSend,
    UserLogin,
    UserRegister,
    VerificationEmailResend,
)
from src.auth.schemas.responses import (
    LoginResponse,
    LogoutResponse,
    RegisterUserResponse,
    ResendVerificationEmailResponse,
    ResetPasswordResponse,
    SendResetPasswordEmailResponse,
    UserResponse,
    VerifyEmailResponse,
)
from src.auth.service import (
    delete_all_user_sessions,
    delete_verifications,
    fetch_credentials_account_by_email,
    fetch_verification_by_value,
    fetch_verifications,
    save_account_password,
    save_session,
    save_verification,
)
from src.database.service import SessionDep
from src.error_handlers.decorators import custom_exception_handler_for_http
from src.errors.models import CustomHttpException
from src.mails.tasks import send_reset_password_email_task, send_verification_email_task
from src.rate_limiter.service import limiter
from src.settings.service import settings
from src.users.models.user import User
from src.users.schemas.internals import CreateUserDto
from src.users.service import fetch_authenticated_user, fetch_user_by_email, save_user
from src.utils.custom_api_route import CustomAPIRoute

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=CustomAPIRoute,
)


@auth_router.post("/register", status_code=201)
@custom_exception_handler_for_http
async def register_user(
    user_register: UserRegister, session: SessionDep, background_tasks: BackgroundTasks
) -> RegisterUserResponse:
    email = user_register.email
    user_with_same_email = await fetch_user_by_email(email, session)
    if user_with_same_email:
        raise CustomHttpException(
            status_code=400, detail=f"User with email '{email}' already exists."
        )

    create_user_dto = CreateUserDto(
        email=user_register.email,
        password=user_register.password,
        name=user_register.name,
        image_url=user_register.image_url,
    )
    user = await save_user(create_user_dto, session)

    create_verification_dto = CreateVerificationDto(
        verification_type=VerificationType.EMAIL_VERIFICATION,
        target=email,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    verification = await save_verification(
        create_verification_dto,
        session,
    )

    await session.commit()

    email = user.email
    token = verification.value
    background_tasks.add_task(send_verification_email_task, email=email, token=token)

    return RegisterUserResponse(detail="User registered successfully.")


@auth_router.post("/resend-verification-email")
@limiter.limit("10/day")
@custom_exception_handler_for_http
async def resend_verification_email(
    request: Request,
    verification_email_resend: VerificationEmailResend,
    session: SessionDep,
    background_tasks: BackgroundTasks,
) -> ResendVerificationEmailResponse:
    email = verification_email_resend.email
    user = await fetch_user_by_email(email, session)

    if user and not user.is_email_verified:
        verification_type = VerificationType.EMAIL_VERIFICATION
        existing_verifications = await fetch_verifications(
            verification_type=verification_type,
            target=email,
            session=session,
        )
        await delete_verifications(existing_verifications, session)

        create_verification_dto = CreateVerificationDto(
            verification_type=verification_type,
            target=email,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        verification = await save_verification(
            create_verification_dto,
            session,
        )

        token = verification.value
        await session.commit()

        background_tasks.add_task(
            send_verification_email_task, email=email, token=token
        )

    return ResendVerificationEmailResponse(
        detail="Verification email resent successfully."
    )


@auth_router.post("/send-reset-password-email")
@limiter.limit("10/day")
@custom_exception_handler_for_http
async def send_reset_password_email(
    request: Request,
    ResetPasswordEmailSend: ResetPasswordEmailSend,
    session: SessionDep,
    background_tasks: BackgroundTasks,
) -> SendResetPasswordEmailResponse:
    email = ResetPasswordEmailSend.email
    user = await fetch_user_by_email(email, session)

    if user:
        verification_type = VerificationType.PASSWORD_RESET
        existing_verifications = await fetch_verifications(
            verification_type=verification_type,
            target=email,
            session=session,
        )
        await delete_verifications(existing_verifications, session)

        create_verification_dto = CreateVerificationDto(
            verification_type=verification_type,
            target=email,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        verification = await save_verification(
            create_verification_dto,
            session,
        )

        token = verification.value
        await session.commit()

        background_tasks.add_task(
            send_reset_password_email_task, email=email, token=token
        )

    return SendResetPasswordEmailResponse(
        detail="Reset password email sent successfully."
    )


@auth_router.post("/verify-email")
@custom_exception_handler_for_http
async def verify_email(
    email_verify: EmailVerify, session: SessionDep
) -> VerifyEmailResponse:
    value = email_verify.token
    verification = await fetch_verification_by_value(
        value=value,
        session=session,
        should_fail=True,
    )

    verification_type, target = VerificationIdentifier.parse(verification.identifier)
    if verification_type != VerificationType.EMAIL_VERIFICATION:
        raise CustomHttpException(
            status_code=400, detail="Invalid email verification token."
        )

    user = await fetch_user_by_email(email=target, session=session, should_fail=True)
    if user.is_email_verified:
        raise CustomHttpException(status_code=400, detail="Email is already verified.")

    user.is_email_verified = True
    session.add(user)

    await delete_verifications([verification], session)

    await session.commit()
    return VerifyEmailResponse(detail="Email verification successful.")


@auth_router.post("/reset-password")
@custom_exception_handler_for_http
async def reset_password(
    password_reset: PasswordReset, session: SessionDep
) -> ResetPasswordResponse:
    value = password_reset.token
    verification = await fetch_verification_by_value(
        value=value,
        session=session,
        should_fail=False,
    )
    if not verification:
        raise CustomHttpException(
            status_code=400, detail="Invalid password reset token."
        )

    verification_type, target = VerificationIdentifier.parse(verification.identifier)
    if verification_type != VerificationType.PASSWORD_RESET:
        raise CustomHttpException(
            status_code=400, detail="Invalid password reset token."
        )

    account = await fetch_credentials_account_by_email(
        email=target, session=session, should_fail=True
    )
    user: User = await account.awaitable_attrs.user
    new_password = password_reset.new_password
    await save_account_password(account=account, password=new_password, session=session)

    await delete_verifications(verifications=[verification], session=session)
    await delete_all_user_sessions(user=user, session=session)

    await session.commit()
    return ResetPasswordResponse(detail="Password reset successful.")


@auth_router.post("/login")
@custom_exception_handler_for_http
async def login(
    request: Request,
    response: Response,
    user_login: UserLogin,
    session: SessionDep,
    user_agent: Annotated[Optional[str], Header()],
) -> LoginResponse:
    email = user_login.email
    password = user_login.password

    user = await fetch_authenticated_user(
        email=email,
        password=password,
        session=session,
        should_fail=True,
    )

    if not user.is_email_verified:
        raise CustomHttpException(
            status_code=400, detail="Email is not verified. Please verify your email."
        )

    create_session_dto = CreateSessionDto(
        ip_address=request.client and request.client.host,
        user_agent=user_agent,
        user=user,
    )
    user_session = await save_session(create_session_dto, session)

    await session.commit()

    response.set_cookie(
        key=Session.KEY_NAME,
        value=user_session.token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.auth.session_expires_in,
    )
    return LoginResponse(**UserResponse.model_construct(**user.__dict__).__dict__)


@auth_router.post("/logout")
@custom_exception_handler_for_http
async def logout(
    response: Response,
    session: SessionDep,
    user: OptionalSessionUser,
) -> LogoutResponse:
    await session.commit()

    response.delete_cookie(
        key=Session.KEY_NAME,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return LogoutResponse(detail="User logged out successfully.")
