from __future__ import annotations
from sqlmodel import SQLModel
from .types import CleanText, OptionalCleanText, PositiveDecimal


class FoodItemBase(SQLModel):
    name: CleanText
    description: OptionalCleanText = None
    price: PositiveDecimal
    is_available: bool = True


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(SQLModel):
    name: CleanText | None = None
    description: OptionalCleanText | None = None
    price: PositiveDecimal | None = None
    is_available: bool | None = None


class FoodItemRead(FoodItemBase):
    id: int
