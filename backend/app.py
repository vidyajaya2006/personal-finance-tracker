from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

DATABASE = os.path.join(
    BASE_DIR,
    "finance.db"
)

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


def init_db():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/transactions", methods=["GET"])
def get_transactions():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, description, amount, type FROM transactions"
    )

    rows = cursor.fetchall()

    conn.close()

    transactions = []

    for row in rows:

        transactions.append({
            "id": row[0],
            "description": row[1],
            "amount": row[2],
            "type": row[3]
        })

    return jsonify(transactions)


@app.route("/transactions", methods=["POST"])
def add_transaction():

    data = request.json

    description = data["description"]
    amount = float(data["amount"])
    transaction_type = data["type"]

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (description, amount, type)
        VALUES (?, ?, ?)
    """, (
        description,
        amount,
        transaction_type
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Transaction added successfully"
    })


@app.route("/summary", methods=["GET"])
def get_summary():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        COALESCE(
            SUM(
                CASE
                WHEN type = 'Income'
                THEN amount
                ELSE 0
                END
            ),
            0
        ),
        COALESCE(
            SUM(
                CASE
                WHEN type = 'Expense'
                THEN amount
                ELSE 0
                END
            ),
            0
        )
        FROM transactions
    """)

    income, expense = cursor.fetchone()

    conn.close()

    balance = income - expense

    return jsonify({
        "income": income,
        "expense": expense,
        "balance": balance
    })


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000
    )