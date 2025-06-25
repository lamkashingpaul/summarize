import secrets
from datetime import datetime, timezone
from typing import Literal, Optional, Sequence, overload

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select

from src.auth.models.account import Account
from src.auth.models.verification import (
    Verification,
    VerificationIdentifier,
    VerificationType,
)
from src.auth.schemas.internals import CreateVerificationDto
from src.database.service import SessionDep
from src.errors.models import (
    CustomDatabaseInternalServerErrorException,
    CustomDatabaseNotFoundException,
)
from src.users.models.user import User


async def save_verification(
    create_verification_dto: CreateVerificationDto, session: SessionDep
) -> Verification:
    verification_type = create_verification_dto.verification_type
    target = create_verification_dto.target
    identifier = VerificationIdentifier.build(
        verification_type=verification_type, target=target
    )
    expires_at = create_verification_dto.expires_at
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

    if not verifications or len(verifications) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Verification with value '{value}' not found"
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
    for verification in verifications:
        await session.delete(verification)


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

    account = accounts[0]
    return account


@overload
async def fetch_authenticated_user_and_credentials_account(
    email: str, password: str, session: SessionDep, should_fail: Literal[True]
) -> tuple[User, Account]: ...
@overload
async def fetch_authenticated_user_and_credentials_account(
    email: str, password: str, session: SessionDep, should_fail: Literal[False] = False
) -> tuple[Optional[User], Optional[Account]]: ...
async def fetch_authenticated_user_and_credentials_account(
    email: str, password: str, session: SessionDep, should_fail: bool = False
) -> tuple[Optional[User], Optional[Account]]:
    account = await fetch_credentials_account_by_email(email, session, should_fail)
    if not account:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' not found"
            )
        return None, None

    user: User = await account.awaitable_attrs.user

    password_hasher = PasswordHasher()
    hashed_password = account.password
    if hashed_password is None:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' has no password set"
            )
        return None, None

    try:
        password_hasher.verify(hashed_password, password)
        if password_hasher.check_needs_rehash(hashed_password):
            account.password = password_hasher.hash(password)
        return user, account

    except VerifyMismatchError as e:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message="Invalid email or password"
            ) from e
        return None, None
    except Exception as e:
        if should_fail:
            raise CustomDatabaseInternalServerErrorException(
                message="An error occurred while verifying the password"
            ) from e
        return None, None
