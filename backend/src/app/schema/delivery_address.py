from __future__ import annotations
from pydantic import field_validator
from sqlmodel import SQLModel
from ..model.enums import PropertyLocationLabel


# =========================================
#       ADDRESS SCHEMA DEFINITIONS                              
# =========================================

class AddressBase(SQLModel):
    """Base schema with shared fields and API-level normalization."""
    label: PropertyLocationLabel
    street: str
    town: str
    city: str
    postal_code: str

    @field_validator("street", "town", "city", mode="before")
    @classmethod
    def normalize_text_fields(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Cannot be empty or just whitespace")
        
        # Title case ensures "new york" becomes "New York", "main street" -> "Main Street"
        return cleaned.title()

    @field_validator("postal_code", mode="before")
    @classmethod
    def normalize_postal_code(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Postal code must be a string")
        
        # Remove internal spaces and force uppercase (e.g., "sw1a 1aa" -> "SW1A1AA")
        cleaned = v.strip().replace(" ", "").upper()
        if len(cleaned) < 3:
            raise ValueError("Postal code is too short")
        
        return cleaned


class AddressCreate(AddressBase):
    """Schema for creating a new address (POST).
    Includes customer_id to link the address to the correct user.
    """
    customer_id: int


class AddressUpdate(SQLModel):
    label: PropertyLocationLabel | None = None
    street: str | None = None
    town: str | None = None
    city: str | None = None
    postal_code: str | None = None


class AddressRead(AddressBase):
    """Schema for returning address data to the client (GET)."""
    id: int
    customer_id: int

