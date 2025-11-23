from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    limit = Column(Float)
    user_id = Column(String, index=True) # Storing username or user_id from Auth Service
    
    expenses = relationship("Expense", back_populates="budget")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    category = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    budget_id = Column(Integer, ForeignKey("budgets.id"))

    budget = relationship("Budget", back_populates="expenses")
