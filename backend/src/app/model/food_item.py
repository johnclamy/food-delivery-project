from typing import Optional
from sqlmodel import Field, SQLModel


# ==========================================
#         FOOD ITEM TABLE DEFINITION                
# ==========================================

class FoodItem(SQLModel, table=True):
    '''Represents a food item to be selected from the menu'''
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float = Field(gt=0)
    is_available: bool = Field(default=True)
