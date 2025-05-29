import pytest
from app.db.connection import get_connection

def pytest_addoption(parser):
    parser.addoption("--test", action="store", default="all", help="Specify test case to run")

@pytest.fixture(autouse=True, scope="function")
def db_cleanup():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")  # Reset DB
        conn.commit()
    except Exception as e:
        print(f"DB cleanup failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()
    yield
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers")  # Reset DB
        conn.commit()
    except Exception as e:
        print(f"DB cleanup failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()