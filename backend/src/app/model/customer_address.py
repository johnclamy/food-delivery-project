from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from backend.src.app.model.customer import Customer
from backend.src.app.model.order import Order


# ===========================================
#      CUSTOMER ADDRESS TABLE DEFINITION                
# ===========================================

class Address(SQLModel, table=True):
    """Represents a specific delivery location saved by a customer."""
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    
    label: str = Field(default="Home") # e.g., "Home", "Work", "Gym"
    full_address: str # You can also split this into street, city, zip if preferred
    is_default: bool = Field(default=False)

    # Relationships
    customer: Optional[Customer] = Relationship(back_populates="addresses")
    orders: List["Order"] = Relationship(back_populates="address")

