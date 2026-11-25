from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel


class CustomerBase(SQLModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None

    @field_validator("phone")
    @classmethod
    def _normalize_phone(cls, v: str) -> str:
        cleaned = "".join(ch for ch in v if ch.isdigit() or ch == "+")
        if len(cleaned) < 7:
            raise ValueError("Phone number is too short")
        return cleaned

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerRead(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime



