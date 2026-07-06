from datetime import datetime, timedelta
import hashlib

from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.core.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
        plain_password,
        hashed_password):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

from jose import JWTError, jwt


def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except JWTError:
        return None

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    
def create_refresh_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

def hash_refresh_token(token: str):

    return hashlib.sha256(
        token.encode()
    ).hexdigest()