import sqlite3


DATABASE = "expenses.db"


def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_expense(amount, expense_date, category):

    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO expenses
        (amount, date, category)
        VALUES (?, ?, ?)
    """, (
        amount,
        expense_date,
        category
    ))

    expense_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return expense_id


def get_all_expenses():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            id,
            amount,
            date,
            category
        FROM expenses
        ORDER BY date DESC, id DESC
    """).fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "amount": row["amount"],
            "date": row["date"],
            "category": row["category"]
        }
        for row in rows
    ]

def delete_expense(expense_id):

    conn = get_connection()

    cursor = conn.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted