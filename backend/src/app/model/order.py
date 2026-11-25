from decimal import Decimal
from datetime import UTC, datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel, ForeignKeyConstraint
from backend.src.app.model.customer import Customer
from backend.src.app.model.address import Address
from backend.src.app.model.enums import OrderStatus
from backend.src.app.model.order_item_link import OrderItemLink


# ==========================================
#       FOOD ORDERING TABLE DEFINITION                
# ==========================================

class Order(SQLModel, table=True):
    '''Represents what a customer would order from the restaurant menu'''
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign keys linking to Customer and Address
    customer_id: int = Field(foreign_key='customer.id', index=True)
    address_id: int = Field(foreign_key='address.id')

    # Order details
    status: OrderStatus = Field(default=OrderStatus.PREPARING, index=True)
    amount: Decimal = Field(max_digits=12, decimal_places=2, gt=0)

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    customer: Optional[Customer] = Relationship(back_populates='orders')
    address: Optional[Address] = Relationship(back_populates='orders')
    items: List['OrderItemLink'] = Relationship(back_populates='order')

    __table_args__ = (
        ForeignKeyConstraint(
            ["address_id", "customer_id"],
            ["address.id", "address.customer_id"],
            name="fk_order_address_belongs_to_customer",
        ),
    )
