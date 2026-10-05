import sqlite3


DATABASE = "expenses.db"


def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def calculate_total():

    conn = get_connection()

    result = conn.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
    """).fetchone()[0]

    conn.close()

    return round(result, 2)


def calculate_categories():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            category,
            SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    conn.close()

    return [
        {
            "category": row["category"],
            "total": round(row["total"], 2)
        }
        for row in rows
    ]


def calculate_monthly():

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            substr(date, 1, 7) AS month,
            SUM(amount) AS total
        FROM expenses
        GROUP BY month
        ORDER BY month
    """).fetchall()

    conn.close()

    return [
        {
            "month": row["month"],
            "total": round(row["total"], 2)
        }
        for row in rows
    ]


def get_dashboard_data():

    return {
        "total_spending": calculate_total(),
        "category_wise": calculate_categories(),
        "monthly": calculate_monthly()
    }