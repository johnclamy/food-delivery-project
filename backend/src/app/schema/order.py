from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import SQLModel

from backend.src.app.model.order import OrderStatus
from backend.src.app.schema.address import AddressSummary
from backend.src.app.schema.order_item_link import OrderItemLinkRead, OrderItemLinkCreate


class OrderBase(SQLModel):
    status: OrderStatus = OrderStatus.PREPARING
    currency: str = "GBP"

    @field_validator("currency")
    @classmethod
    def _validate_currency(cls, v: str) -> str:
        if len(v) != 3 or not v.isalpha():
            raise ValueError("currency must be ISO 4217 (e.g. 'GBP', 'USD')")
        return v.upper()


class OrderCreate(OrderBase):
    """Payload for POST /orders.

    Note: `amount` is NOT accepted from the client — it must be computed
    server-side from `items` to prevent price tampering.
    """
    customer_id: int
    address_id: int
    items: List[OrderItemLinkCreate] = []



class OrderUpdate(SQLModel):
    """Payload for PATCH — only status is client-mutable; everything else is system-owned."""
    status: Optional[OrderStatus] = None


class OrderRead(OrderBase):
    id: int
    customer_id: int
    address_id: int
    amount: Decimal
    reference: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # Embedded views
    address: Optional[AddressSummary] = None
    items: List[OrderItemLinkRead] = []


class OrderSummary(SQLModel):
    """Lightweight version for embedding in Customer responses."""
    id: int
    status: OrderStatus
    amount: Decimal
    currency: str
    created_at: datetime