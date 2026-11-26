from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Index, Numeric, func
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, ForeignKeyConstraint
from backend.src.app.model.enums import OrderStatus

if TYPE_CHECKING:
    from backend.src.app.model.customer import Customer
    from backend.src.app.model.address import Address
    from backend.src.app.model.order_item_link import OrderItemLink


# ==========================================
#       FOOD ORDERING TABLE DEFINITION                
# ==========================================

class Order(SQLModel, table=True):
    '''Represents what a customer would order from the restaurant menu'''

    __tablename__ = "orders" # type: ignore
    __table_args__ = (
        ForeignKeyConstraint(
            ["address_id", "customer_id"],
            ["address.id", "address.customer_id"],
            name="fk_order_address_belongs_to_customer",
        ),
        Index("ix_order_customer_id", "customer_id"),
        Index("ix_order_address_id", "address_id"),
        Index("ix_order_status", "status"),
        Index("ix_order_created_at", "created_at"),
        # Common access pattern: "customer's latest orders"
        Index("ix_order_customer_created", "customer_id", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys linking to Customer and Address
    customer_id: int = Field(
        foreign_key="customer.id",
        nullable=False,
        ondelete="RESTRICT",   # don't lose orders if a customer row is deleted
    )
    address_id: int = Field(
        foreign_key="address.id",
        nullable=False,
        ondelete="RESTRICT",   # addresses referenced by orders can't be hard-deleted
    )

    # Order details
    status: OrderStatus = Field(default=OrderStatus.PREPARING, index=True)

    # Money as Decimal — never float. `amount` = total, `currency` = ISO 4217.
    amount: Decimal = Field(
        max_digits=12,
        decimal_places=2,
        sa_column=Column(Numeric(12, 2), nullable=False),
    )
    currency: str = Field(default="GBP", max_length=3)

    # Optional reference / receipt number for external systems.
    reference: Optional[str] = Field(default=None, max_length=64, unique=True, index=True)

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
    customer: Optional["Customer"] = Relationship(back_populates="orders")
    address: Optional["Address"] = Relationship(back_populates="orders")
    items: List["OrderItemLink"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
