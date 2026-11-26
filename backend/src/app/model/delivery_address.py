from __future__ import annotations
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from backend.src.app.model.enums import PropertyLocationLabel


# =========================================
#       RELATIVE IMPORTS (TYPE CHECKING)
# =========================================
if TYPE_CHECKING:
    from .customers import Customer
    from .orders import Order


# ===========================================
#      CUSTOMER ADDRESS TABLE DEFINITION                
# ===========================================

class Address(SQLModel, table=True):
    """Represents a specific delivery location saved by a customer."""

    __tablename__ = "delivery_addresses" # type: ignore
    __table_args__ = (
        # A customer can't have two addresses with the same label ("Home" twice).
        UniqueConstraint("customer_id", "label", name="uq_address_customer_label"),
    )

    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(
        foreign_key="customers.id",
        nullable=False,
        ondelete="CASCADE",
    )
    
    label: PropertyLocationLabel = Field(default=PropertyLocationLabel.HOME)
    street: str= Field(max_length=200)
    town: str = Field(max_length=120)
    city: str = Field(max_length=120)
    postal_code: str = Field(max_length=32)

    # Relationships
    customer: Customer = Relationship(back_populates="addresses")
    orders: list["Order"] = Relationship(
        back_populates="address",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
