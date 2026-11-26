from decimal import Decimal
from sqlmodel import Field, SQLModel


# ==========================================
#         FOOD ITEM TABLE DEFINITION                
# ==========================================

class FoodItem(SQLModel, table=True):
    '''Represents a food item to be selected from the menu'''
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)
    is_available: bool = Field(default=True)
