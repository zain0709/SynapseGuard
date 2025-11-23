from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError

from . import models, schemas, database, external_api

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Budget Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to validate token (simple validation, in real world verify signature with public key or shared secret)
# Here we assume shared secret for simplicity or just decoding if we trust the internal network
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

@app.post("/budgets/", response_model=schemas.Budget)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    db_budget = models.Budget(**budget.dict(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

@app.get("/budgets/", response_model=List[schemas.Budget])
def read_budgets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    budgets = db.query(models.Budget).filter(models.Budget.user_id == user_id).offset(skip).limit(limit).all()
    return budgets

@app.post("/budgets/{budget_id}/expenses/", response_model=schemas.Expense)
def create_expense(budget_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    # Verify budget belongs to user
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db_expense = models.Expense(**expense.dict(), budget_id=budget_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.put("/budgets/{budget_id}", response_model=schemas.Budget)
def update_budget(budget_id: int, budget: schemas.BudgetCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db_budget.name = budget.name
    db_budget.limit = budget.limit
    db.commit()
    db.refresh(db_budget)
    return db_budget

@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(db_budget)
    db.commit()
    return {"message": "Budget deleted successfully"}

@app.put("/budgets/{budget_id}/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(budget_id: int, expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    # Verify budget belongs to user
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.budget_id == budget_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db_expense.description = expense.description
    db_expense.amount = expense.amount
    db_expense.category = expense.category
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.delete("/budgets/{budget_id}/expenses/{expense_id}")
def delete_expense(budget_id: int, expense_id: int, db: Session = Depends(database.get_db), user_id: str = Depends(get_current_user)):
    # Verify budget belongs to user
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.budget_id == budget_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}

@app.get("/rates/{currency}")
def get_rates(currency: str):
    return external_api.get_exchange_rates(currency)

