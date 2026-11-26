from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint
from sqlmodel import Field, Relationship, SQLModel


# =========================================
#       RELATIVE IMPORTS (TYPE CHECKING)
# =========================================
if TYPE_CHECKING:
    from .food_item import FoodItem
    from .orders import Order


# ==========================================
#      ORDER ITEM LINK TABLE DEFINITION
# ==========================================

class OrderItemLink(SQLModel, table=True):
    """
    Association object between Order and FoodItem, carrying per-line data.

    Composite PK (order_id, food_item_id) enforces:
    - An order may contain at most one line per food item.
    - To order N units of the same item, use a single line with quantity=N.
    - A food item may appear in many different orders (one line per order).
    """

    __tablename__ = "order_item_links"  # type: ignore
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_item_links_quantity_positive"),
        CheckConstraint("unit_price > 0", name="ck_order_item_links_unit_price_positive"),
    )
    
    order_id: int = Field(
        foreign_key="orders.id",
        primary_key=True,
        ondelete="CASCADE",
    )    
    food_item_id: int = Field(
        foreign_key="food_items.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)

    # --- Relationships ---
    order: "Order" = Relationship(back_populates="items")
    food_item: "FoodItem" = Relationship()
