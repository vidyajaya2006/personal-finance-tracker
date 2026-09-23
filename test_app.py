import os
import tempfile

from backend.app import app
import backend.app as app_module


def test_home_page():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_add_transaction():

    database_file = tempfile.NamedTemporaryFile(
        delete=False
    )

    database_file.close()

    old_database = app_module.DATABASE

    app_module.DATABASE = database_file.name

    app_module.init_db()

    client = app.test_client()

    response = client.post(
        "/transactions",
        json={
            "description": "Test Food",
            "amount": 100,
            "type": "Expense"
        }
    )

    assert response.status_code == 200

    response = client.get("/transactions")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1

    assert data[0]["description"] == "Test Food"

    app_module.DATABASE = old_database

    os.remove(database_file.name)


def test_summary():

    database_file = tempfile.NamedTemporaryFile(
        delete=False
    )

    database_file.close()

    old_database = app_module.DATABASE

    app_module.DATABASE = database_file.name

    app_module.init_db()

    client = app.test_client()

    client.post(
        "/transactions",
        json={
            "description": "Salary",
            "amount": 10000,
            "type": "Income"
        }
    )

    client.post(
        "/transactions",
        json={
            "description": "Food",
            "amount": 500,
            "type": "Expense"
        }
    )

    response = client.get("/summary")

    assert response.status_code == 200

    data = response.get_json()

    assert data["income"] == 10000

    assert data["expense"] == 500

    assert data["balance"] == 9500

    app_module.DATABASE = old_database

    os.remove(database_file.name)