from __future__ import annotations
from sqlmodel import SQLModel
from ..model.enums import PropertyLocationLabel
from .types import CleanText, OptionalCleanText, CleanPostalCode, OptionalCleanPostalCode


# =========================================
#       ADDRESS SCHEMA DEFINITIONS                              
# =========================================

class AddressBase(SQLModel):
    """Base schema with shared fields and API-level normalization."""
    label: PropertyLocationLabel
    street:CleanText 
    town: CleanText
    city: CleanText
    postal_code: CleanPostalCode


class AddressCreate(AddressBase):
    """Schema for creating a new address (POST).
    Includes customer_id to link the address to the correct user.
    """
    customer_id: int


class AddressUpdate(SQLModel):
    """Schema for creating a new address (UPDATE)."""
    label: PropertyLocationLabel | None = None
    street: OptionalCleanText = None
    town: OptionalCleanText = None
    city: OptionalCleanText = None
    postal_code: OptionalCleanPostalCode = None


class AddressRead(AddressBase):
    """Schema for returning address data to the client (GET)."""
    id: int
    customer_id: int
