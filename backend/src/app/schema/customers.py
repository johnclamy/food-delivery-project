from __future__ import annotations
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel
from .types import PhoneNumber, OptionalPhoneNumber, CleanText, OptionalCleanText


class CustomerBase(SQLModel):
    """Base schema with shared fields and API-level validators."""
    name: CleanText
    phone: PhoneNumber
    email: EmailStr | None = None


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer (POST)."""
    pass


class CustomerUpdate(SQLModel):
    name: OptionalCleanText = None
    phone: OptionalPhoneNumber = None
    email: EmailStr | None = None


class CustomerRead(CustomerBase):
    """Schema for returning customer data to the client (GET)."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
