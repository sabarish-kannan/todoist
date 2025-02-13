"""Auth schemas."""

from pydantic import BaseModel


class SignUpRequest(BaseModel):
    """Sign up request schema."""

    username: str
    email: str
    password: str


class SignUpResponse(BaseModel):
    """Sign up response schema."""

    id: int
    username: str
    email: str


class LoginRequest(BaseModel):
    """Login request schema."""

    email: str
    password: str


class LoginResponse(BaseModel):
    """Login response schema."""

    access_token: str
    token_type: str
