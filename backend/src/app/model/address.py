from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Index, func
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from backend.src.app.model.customer import Customer
    from backend.src.app.model.enums import PropertyLocationLabel
    from backend.src.app.model.order import Order


# ===========================================
#      CUSTOMER ADDRESS TABLE DEFINITION                
# ===========================================

class Address(SQLModel, table=True):
    """Represents a specific delivery location saved by a customer."""

    __tablename__ = "address" # type: ignore
    __table_args__ = (
        # A customer can't have two addresses with the same label ("Home" twice).
        UniqueConstraint("customer_id", "label", name="uq_address_customer_label"),
        # Fast lookup of a customer's addresses.
        Index("ix_address_customer_id", "customer_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(
        foreign_key="customer.id",
        nullable=False,
        ondelete="CASCADE",
    )
    
    label: PropertyLocationLabel = Field(default=PropertyLocationLabel.HOME)
    number: str
    street: str
    city: str
    postcode: str
    is_default: bool = Field(default=False)

    # Relationships
    customer: Optional[Customer] = Relationship(back_populates="addresses")
    orders: List["Order"] = Relationship(back_populates="address")

    __table_args__ = (
        UniqueConstraint("id", "customer_id", name="uq_address_id_customer"),
    )
