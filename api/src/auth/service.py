import secrets
from datetime import datetime, timezone
from typing import Literal, Optional, Sequence, overload

from argon2 import PasswordHasher
from sqlalchemy import select

from src.auth.models.account import Account
from src.auth.models.verification import Verification
from src.auth.schemas.internals import CreateVerificationDto
from src.database.service import SessionDep
from src.errors.models import CustomDatabaseNotFoundException
from src.users.models.user import User


async def save_verification(
    create_verification_dto: CreateVerificationDto, session: SessionDep
) -> Verification:
    identifier = create_verification_dto.identifier
    expires_at = create_verification_dto.expires_at
    value = ""

    while True:
        value = secrets.token_hex(16)
        statement = select(Verification).where(
            Verification.value == value,
            Verification.identifier == identifier,
        )
        result = await session.scalars(statement)
        verifications = result.all()
        if not verifications:
            break

    verification = Verification(
        identifier=identifier,
        value=value,
        expires_at=expires_at,
    )
    session.add(verification)

    return verification


@overload
async def fetch_verification_by_identifier_and_value(
    identifier: str, value: str, session: SessionDep, should_fail: Literal[True]
) -> Verification: ...
@overload
async def fetch_verification_by_identifier_and_value(
    identifier: str,
    value: str,
    session: SessionDep,
    should_fail: Literal[False] = False,
) -> Optional[Verification]: ...
async def fetch_verification_by_identifier_and_value(
    identifier: str, value: str, session: SessionDep, should_fail: bool = False
) -> Optional[Verification]:
    statement = (
        select(Verification)
        .where(
            Verification.identifier == identifier,
            Verification.value == value,
            Verification.expires_at > datetime.now(timezone.utc),
        )
        .limit(2)
    )
    result = await session.scalars(statement)
    verifications = result.all()

    if not verifications or len(verifications) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Verification with identifier '{identifier}' and value '{value}' not found"
            )
        return None

    return verifications[0]


async def fetch_verifications_by_identifier(identifier: str, session: SessionDep):
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
    await session.delete(verifications)


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
            User.is_email_verified.is_(True),
            Account.provider_id == "credentials",
        )
        .limit(2)
    )
    result = await session.scalars(statement)
    accounts = result.all()
    if not accounts or len(accounts) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' not found"
            )
        return None

    return accounts[0]


@overload
async def fetch_authenticated_user(
    email: str, password: str, session: SessionDep, should_fail: Literal[True]
) -> User: ...
@overload
async def fetch_authenticated_user(
    email: str, password: str, session: SessionDep, should_fail: Literal[False] = False
) -> Optional[User]: ...
async def fetch_authenticated_user(
    email: str, password: str, session: SessionDep, should_fail: bool = False
) -> Optional[User]:
    account = await fetch_credentials_account_by_email(email, session, should_fail)
    if not account:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' not found"
            )
        return None

    user = await account.awaitable_attrs.user

    password_hasher = PasswordHasher()
    hashed_password = account.password
    if hashed_password is None:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' has no password set"
            )
        return None

    try:
        password_hasher.verify(hashed_password, password)
        if password_hasher.check_needs_rehash(hashed_password):
            account.password = password_hasher.hash(password)
        return user
    except Exception:
        if should_fail:
            raise CustomDatabaseNotFoundException(message="Invalid email or password")
        return None
