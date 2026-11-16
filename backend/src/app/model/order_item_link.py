from decimal import Decimal
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from backend.src.app.model.food_item import FoodItem
from backend.src.app.model.order import Order


# ==========================================
#      ORDER ITEM LINK TABLE DEFINITION                
# ==========================================

class OrderItemLink(SQLModel, table=True):
    """Link table for Order and FoodItem."""
    order_id: Optional[int] = Field(default=None, foreign_key="order.id", primary_key=True)
    food_item_id: Optional[int] = Field(default=None, foreign_key="fooditem.id", primary_key=True)
    
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)

    order: Optional[Order] = Relationship(back_populates="items")
    food_item: Optional[FoodItem] = Relationship()
