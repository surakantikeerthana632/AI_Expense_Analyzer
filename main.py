from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

from database import (
    initialize_database,
    save_expense,
    get_all_expenses,
    delete_expense
)

from analytics import get_dashboard_data
from ai_analysis import analyze_expenses


app = FastAPI(title="AI Expense Analyzer")


# Initialize database when application starts
initialize_database()


# Serve frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")


class Expense(BaseModel):
    amount: float = Field(gt=0)
    date: date
    category: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "AI Expense Analyzer is running",
        "open": "/static/index.html"
    }


# Add expense
@app.post("/expenses")
def add_expense(expense: Expense):

    try:
        expense_id = save_expense(
            expense.amount,
            str(expense.date),
            expense.category
        )

        return {
            "status": "success",
            "message": "Expense added successfully",
            "expense": {
                "id": expense_id,
                "amount": expense.amount,
                "date": str(expense.date),
                "category": expense.category
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not save expense: {str(e)}"
        )


# Get all expenses
@app.get("/expenses")
def expenses():

    try:
        return {
            "status": "success",
            "expenses": get_all_expenses()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Delete expense
@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int):

    try:
        deleted = delete_expense(expense_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        return {
            "status": "success",
            "message": "Expense deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# Dashboard analytics
@app.get("/dashboard")
def dashboard():
    try:
        return {
            "status": "success",
            "data": get_dashboard_data()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# AI insights
@app.get("/ai-insights")
async def ai_insights():

    try:
        expense_data = get_all_expenses()

        result = await analyze_expenses(expense_data)

        return {
            "status": "success",
            "insights": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )