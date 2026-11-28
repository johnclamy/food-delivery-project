from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from pydantic import Field
from sqlmodel import SQLModel

from ..model.enums import OrderStatus
from .types import CurrencyCode, OptionalReferenceCode, PositiveDecimal, ReferenceCode
from .order_item_link import OrderItemCreate, OrderItemRead


class OrderBase(SQLModel):
    """Fields that represent the core state of an order."""
    customer_id: int
    address_id: int
    status: OrderStatus
    amount: PositiveDecimal
    currency: CurrencyCode
    reference: ReferenceCode | None = None


class OrderCreate(SQLModel):
    """
    Schema for creating a new order (POST).
    SECURITY: Client does NOT send 'amount', 'currency', or 'status'.
    The backend calculates the total amount from the items and defaults 
    status to PREPARING.
    """
    customer_id: int
    address_id: int
    reference: ReferenceCode | None = None
    items: list[OrderItemCreate] = Field(
        min_length=1, 
        description="An order must contain at least one item"
    )


class OrderUpdate(SQLModel):
    """
    Schema for updating an existing order (PATCH).
    Typically used by staff/driver apps to advance the status, 
    or to add a delivery reference.
    """
    status: OrderStatus | None = None
    reference: ReferenceCode | None = None


class OrderRead(OrderBase):
    """Schema for returning order data to the client (GET)."""
    id: int
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead] = Field(default_factory=list)
