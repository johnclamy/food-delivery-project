from decimal import Decimal
from sqlalchemy import CheckConstraint
from sqlmodel import Field, SQLModel


# ==========================================
#         FOOD ITEM TABLE DEFINITION                
# ==========================================

class FoodItem(SQLModel, table=True):
    '''Represents a food item to be selected from the menu'''

    __tablename__ = "food_items"  # type: ignore
    __table_args__ = (
        CheckConstraint("price > 0", name="ck_food_items_price_positive"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)
    is_available: bool = Field(default=True, index=True)
