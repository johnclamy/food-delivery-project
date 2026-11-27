from __future__ import annotations
from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel


class CustomerBase(SQLModel):
    """Base schema with shared fields and API-level validators."""
    name: str
    phone: str
    email: EmailStr | None = None

    @field_validator("phone", mode="before")
    @classmethod
    def _normalize_phone(cls, v: str) -> str:
        # Guard against non-string types (e.g., if a client accidentally sends an int)
        if not isinstance(v, str):
            raise ValueError("Phone number must be a string")
        
        cleaned = "".join(ch for ch in v if ch.isdigit() or ch == "+")
        if len(cleaned) < 7:
            raise ValueError("Phone number is too short (minimum 7 digits)")
        return cleaned

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Name must be a string")
        
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Name cannot be empty or just whitespace")
        return cleaned


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer (POST)."""
    pass


class CustomerUpdate(SQLModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None


class CustomerRead(CustomerBase):
    """Schema for returning customer data to the client (GET)."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
