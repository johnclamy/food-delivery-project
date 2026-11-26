from __future__ import annotations
from datetime import UTC, datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Index, func
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.src.app.model.address import Address
    from backend.src.app.model.orders import Order


# =========================================
#         CUSTOMER TABLE DEFINITION                              
# =========================================

class Customer(SQLModel, table=True):
    """Represents the user/guest placing the order."""

    __tablename__ = "customer" # type: ignore
    __table_args__ = (
        Index("ix_customer_phone", func.lower("phone")),
        Index("ix_customer_created_at", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=120)
    phone: str = Field(unique=True, max_length=20)
    email: Optional[str] = Field(
        default=None,
        max_length=154,
        index=True,
        unique=True
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
    addresses: List["Address"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    orders: List["Order"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
