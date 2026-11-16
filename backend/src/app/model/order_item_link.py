from decimal import Decimal
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from backend.src.app.model.food_item import FoodItem
from backend.src.app.model.order import Order


# ==========================================
#      ORDER ITEM LINK TABLE DEFINITION                
# ==========================================

class OrderItemLink(SQLModel, table=True):
    """
    Association object between Order and FoodItem, carrying per-line data.

    Composite PK (order_id, food_item_id) enforces:
      - An order may contain **at most one line per food item**.
      - To order N units of the same item, use a single line with quantity=N.
      - A food item may appear in many different orders (one line per order).

    Deleting an order or a food item cascades to its link rows.
    """
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    food_item_id: int = Field(foreign_key="fooditem.id", primary_key=True)
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)

    order: Optional[Order] = Relationship(back_populates="items")
    food_item: Optional[FoodItem] = Relationship()
