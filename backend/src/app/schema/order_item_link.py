from __future__ import annotations
from pydantic import Field
from sqlmodel import SQLModel
from .types import PositiveDecimal


class OrderItemBase(SQLModel):
    food_item_id: int
    quantity: int = Field(gt=0, description="Must be at least 1")
    # NOTE: unit_price is intentionally OMITTED from Create. 
    # The backend service must fetch the FoodItem.price and set this 
    # to prevent client-side price manipulation.


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    unit_price: PositiveDecimal
    
    # Optional: Nest the food item details so the frontend can display 
    # the name and description on the receipt without extra API calls.
    food_item: FoodItemRead | None = None 


# Forward reference resolution
from .food_item import FoodItemRead
OrderItemRead.model_rebuild()
