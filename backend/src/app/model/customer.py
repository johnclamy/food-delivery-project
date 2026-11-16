from datetime import UTC, datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from backend.src.app.model.customer_address import Address
from backend.src.app.model.order import Order


# =========================================
#         CUSTOMER TABLE DEFINITION                              
# =========================================

class Customer(SQLModel, table=True):
    """Represents the user/guest placing the order."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    email: Optional[str] = Field(default=None, index=True, unique=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    addresses: List["Address"] = Relationship(back_populates="customer")
    orders: List["Order"] = Relationship(back_populates="customer")
