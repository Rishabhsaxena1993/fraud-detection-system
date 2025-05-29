import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_get import GetTests
from tests.test_post import PostTests
from tests.test_uploads import UploadTests

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    return client

class TestAPI:
    @pytest.mark.parametrize("test_name", [
        "test_get_customer",
        "test_get_customer_invalid_id",
        "test_get_invalid_endpoint",
        "test_get_customers_valid_endpoint",
        "test_get_list_of_records_and_print",
        "test_get_list_of_duplicate_records",
        "test_get_users_fraud_code_1",
        "test_get_users_fraud_code_2",
        "test_post_single_fraud_code_1",
        "test_post_single_fraud_code_2",
        "test_post_invalid_fraud_code",
        "test_post_multiple_customers",
        "test_post_upload_document",
    ])
    def test_run_selected(self, test_name, test_client, pytestconfig):
        test_option = pytestconfig.getoption("test")
        if test_option != "all" and test_option != test_name:
            pytest.skip(f"Skipping {test_name}, running {test_option}")
        try:
            if test_name.startswith("test_get"):
                get_tests = GetTests(test_client)
                getattr(get_tests, test_name)()
            elif test_name.startswith("test_post_single") or test_name == "test_post_multiple_customers":
                post_tests = PostTests(test_client)
                getattr(post_tests, test_name)()
            elif test_name == "test_post_upload_document":
                upload_tests = UploadTests(test_client)
                getattr(upload_tests, test_name)()
        except Exception as e:
            print(f"Test {test_name} failed with error: {str(e)}")
            raise