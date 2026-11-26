from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Index, func, text
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


# =========================================
#       RELATIVE IMPORTS (TYPE CHECKING)
# =========================================
if TYPE_CHECKING:
    from .delivery_address import Address
    from .orders import Order


# =========================================
#         CUSTOMER TABLE DEFINITION                              
# =========================================

class Customer(SQLModel, table=True):
    """Represents the user/guest placing the order."""

    __tablename__ = "customers" # type: ignore
    __table_args__ = (
        Index("ix_customers_lower_phone", text("lower(phone)")),
        Index("ix_customers_created_at", "created_at"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=120)
    phone: str = Field(max_length=20)
    email: str | None = Field(
        default=None,
        max_length=154,
        index=True,
        unique=True,
    )

    # --- Soft-delete / status ---
    is_active: bool = Field(default=True, index=True)
    
    # Timestamps
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        ),
    )

    # Relationships
    addresses: list["Address"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    orders: list["Order"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
