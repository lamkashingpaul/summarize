from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Request

from src.auth.schemas.internals import CreateVerificationDto
from src.auth.schemas.requests import (
    EmailVerify,
    UserLogin,
    UserRegister,
    VerificationEmailResend,
)
from src.auth.schemas.responses import (
    RegisterUserResponse,
    ResendVerificationEmailResponse,
    UserLoginResponse,
    UserResponse,
    VerifyEmailResponse,
)
from src.auth.service import (
    delete_verifications,
    fetch_authenticated_user,
    fetch_verification_by_identifier_and_value,
    fetch_verifications_by_identifier,
    save_verification,
)
from src.database.service import SessionDep
from src.error_handlers.decorators import custom_exception_handler_for_http
from src.errors.models import CustomHttpException
from src.mails.tasks import send_verification_email_task
from src.rate_limiter.service import limiter
from src.users.schemas.internals import CreateUserDto
from src.users.service import fetch_user_by_email, save_user
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
        identifier=email,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
    )
    verification = await save_verification(
        create_verification_dto,
        session,
    )

    await session.commit()

    email = user.email
    token = verification.value
    background_tasks.add_task(send_verification_email_task, email=email, token=token)

    return RegisterUserResponse(message="User registered successfully.")


@auth_router.post("/verify-email")
@limiter.limit("10/day")
@custom_exception_handler_for_http
async def verify_email(
    request: Request, email_verify: EmailVerify, session: SessionDep
) -> VerifyEmailResponse:
    identifier = email = email_verify.email
    value = email_verify.token
    verification = await fetch_verification_by_identifier_and_value(
        identifier=identifier,
        value=value,
        session=session,
        should_fail=True,
    )

    user = await fetch_user_by_email(email, session, should_fail=True)
    if user.is_email_verified:
        raise CustomHttpException(status_code=400, detail="Email is already verified.")

    user.is_email_verified = True
    session.add(user)

    await delete_verifications([verification], session)
    await session.commit()

    return VerifyEmailResponse(message="Email verification successful.")


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
        existing_verifications = await fetch_verifications_by_identifier(
            identifier=email, session=session
        )
        await delete_verifications(existing_verifications, session)

        create_verification_dto = CreateVerificationDto(
            identifier=email,
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        )
        verification = await save_verification(
            create_verification_dto,
            session,
        )

        token = verification.value
        background_tasks.add_task(
            send_verification_email_task, email=email, token=token
        )

    return ResendVerificationEmailResponse(
        message="Verification email resent successfully."
    )


@auth_router.post("/login")
@custom_exception_handler_for_http
async def login_user(
    user_login: UserLogin, session: SessionDep, background_tasks: BackgroundTasks
) -> UserLoginResponse:
    email = user_login.email
    password = user_login.password

    user = await fetch_authenticated_user(
        email=email,
        password=password,
        session=session,
        should_fail=True,
    )

    await session.commit()
    return UserLoginResponse(**UserResponse.model_construct(**user.__dict__).__dict__)
