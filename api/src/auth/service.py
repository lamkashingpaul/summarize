import secrets
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional, Sequence, overload

from argon2 import PasswordHasher
from sqlalchemy import delete, select

from src.auth.models.account import Account
from src.auth.models.session import Session
from src.auth.models.verification import (
    Verification,
    VerificationIdentifier,
    VerificationType,
)
from src.auth.schemas.internals import CreateSessionDto, CreateVerificationDto
from src.database.service import SessionDep
from src.errors.models import (
    CustomDatabaseNotFoundException,
)
from src.settings.service import settings
from src.users.models.user import User


async def generate_unique_verification_value(identifier: str, session: SessionDep):
    value = ""

    while True:
        value = secrets.token_hex(16)
        statement = (
            select(Verification)
            .where(
                Verification.value == value,
                Verification.identifier == identifier,
            )
            .limit(1)
        )
        result = await session.scalars(statement)
        verifications = result.all()
        if not verifications:
            break

    return value


async def generate_unique_session_token(session: SessionDep):
    token = ""

    while True:
        token = secrets.token_hex(16)
        statement = select(Session).where(Session.token == token).limit(1)
        result = await session.scalars(statement)
        sessions = result.all()
        if not sessions:
            break

    return token


async def save_verification(
    create_verification_dto: CreateVerificationDto, session: SessionDep
) -> Verification:
    verification_type = create_verification_dto.verification_type
    target = create_verification_dto.target
    identifier = VerificationIdentifier.build(
        verification_type=verification_type, target=target
    )
    expires_at = create_verification_dto.expires_at
    value = await generate_unique_verification_value(
        identifier=identifier, session=session
    )

    verification = Verification(
        identifier=identifier,
        value=value,
        expires_at=expires_at,
    )
    session.add(verification)

    return verification


@overload
async def fetch_verification_by_value(
    value: str, session: SessionDep, should_fail: Literal[True]
) -> Verification: ...
@overload
async def fetch_verification_by_value(
    value: str,
    session: SessionDep,
    should_fail: Literal[False] = False,
) -> Optional[Verification]: ...
async def fetch_verification_by_value(
    value: str, session: SessionDep, should_fail: bool = False
) -> Optional[Verification]:
    statement = (
        select(Verification)
        .where(
            Verification.value == value,
            Verification.expires_at > datetime.now(timezone.utc),
        )
        .limit(2)
    )
    result = await session.scalars(statement)
    verifications = result.all()

    if len(verifications) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Verification with value '{value}' not found."
            )
        return None

    return verifications[0]


async def fetch_verifications(
    verification_type: VerificationType, target: str, session: SessionDep
):
    identifier = VerificationIdentifier.build(
        verification_type=verification_type, target=target
    )

    statement = select(Verification).where(
        Verification.identifier == identifier,
        Verification.expires_at > datetime.now(timezone.utc),
    )
    result = await session.scalars(statement)
    verifications = result.all()
    return verifications


async def delete_verifications(
    verifications: Sequence[Verification], session: SessionDep
):
    verification_ids = [verification.id for verification in verifications]
    statement = delete(Verification).where(Verification.id.in_(verification_ids))
    await session.execute(statement)


@overload
async def fetch_credentials_account_by_email(
    email: str, session: SessionDep, should_fail: Literal[True]
) -> Account: ...
@overload
async def fetch_credentials_account_by_email(
    email: str, session: SessionDep, should_fail: Literal[False] = False
) -> Optional[Account]: ...
async def fetch_credentials_account_by_email(
    email: str, session: SessionDep, should_fail: bool = False
) -> Optional[Account]:
    statement = (
        select(Account)
        .join(Account.user)
        .where(
            User.email == email,
            Account.provider_id == "credentials",
        )
        .limit(2)
    )
    result = await session.scalars(statement)
    accounts = result.all()
    if len(accounts) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' not found."
            )
        return None

    account = accounts[0]
    return account


async def save_account_password(account: Account, password: str, session: SessionDep):
    password_hasher = PasswordHasher()
    account.password = password_hasher.hash(password)
    session.add(account)


async def delete_all_user_sessions(user: User, session: SessionDep):
    statement = delete(Session).where(Session.user_id == user.id)
    await session.execute(statement)


async def save_session(create_session_dto: CreateSessionDto, session: SessionDep):
    session_expires_in = settings.auth.session_expires_in
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=session_expires_in)
    token = await generate_unique_session_token(session)

    user_session = Session(
        expires_at=expires_at,
        token=token,
        ip_address=create_session_dto.ip_address,
        user_agent=create_session_dto.user_agent,
        user=create_session_dto.user,
    )
    session.add(user_session)
    return user_session
