from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: str

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    date: datetime
    budget_id: int

    class Config:
        orm_mode = True

class BudgetBase(BaseModel):
    name: str
    limit: float

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: str
    expenses: List[Expense] = []

    class Config:
        orm_mode = True
