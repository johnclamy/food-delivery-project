from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, Index, Numeric, func
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel
from backend.src.app.model.enums import OrderStatus


# =========================================
#       RELATIVE IMPORTS (TYPE CHECKING)
# =========================================
if TYPE_CHECKING:
    from .customers import Customer
    from .delivery_address import Address
    from .order_item_link import OrderItemLink


# ==========================================
#       FOOD ORDERING TABLE DEFINITION                
# ==========================================

class Order(SQLModel, table=True):
    '''Represents what a customer would order from the restaurant menu'''

    __tablename__ = "orders" # type: ignore
    __table_args__ = (
        ForeignKeyConstraint(  # *** Requires PRAGMA foreign_keys = ON in SQLite ***
            ["address_id", "customer_id"],
            ["delivery_addresses.id", "delivery_addresses.customer_id"],
            name="fk_order_address_belongs_to_customer",
        ),
        CheckConstraint("amount > 0", name="ck_orders_amount_positive"),
        Index("ix_order_address_id", "address_id"),
        Index("ix_order_created_at", "created_at"),
        # Common access pattern: "customer's latest orders"
        Index("ix_order_customer_created", "customer_id", "created_at"),
    )

    id: int | None = Field(default=None, primary_key=True)

    # Foreign keys linking to Customer and Address
    customer_id: int = Field(
        foreign_key="customers.id",
        nullable=False,
        ondelete="RESTRICT",   # Don't lose orders if a customer row is deleted
    )
    address_id: int = Field(
        foreign_key="delivery_addresses.id",
        nullable=False,
        ondelete="RESTRICT",   # Addresses referenced by orders can't be hard-deleted
    )

    # Order details
    status: OrderStatus = Field(default=OrderStatus.PREPARING, index=True)

    # Money as Decimal — never float. `amount` = total, `currency` = ISO 4217.
    amount: Decimal = Field(
        sa_column=Column(Numeric(12, 2), nullable=False),
    )
    currency: str = Field(default="GBP", max_length=3)

    # Optional reference / receipt number for external systems.
    reference: str | None = Field(default=None, max_length=64, unique=True)

    # --- Timestamps (timezone-aware, server defaults) ---
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )

    # --- Relationships ---
    customer: "Customer" = Relationship(back_populates="orders")
    address: "Address" = Relationship(back_populates="orders")
    items: list["OrderItemLink"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
