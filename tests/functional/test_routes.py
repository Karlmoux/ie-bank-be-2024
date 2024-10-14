from iebank_api import app
import pytest

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Lebanon'})
    assert response.status_code == 200
    
def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the response is valid and the account no longer exists
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Charlie',
        'currency': '$',
        'country': 'USA'
    })
    assert create_response.status_code == 200, (
        f"Failed to create account. Status: {create_response.status_code}, "
        f"Response: {create_response.data.decode('utf-8')}"
    )
    account_data = create_response.get_json()
    assert account_data is not None, "Create response didn't return JSON data"
    assert 'id' in account_data, f"'id' not found in create response. Data: {account_data}"
    account_id = account_data['id']

    # Now, delete the account
    delete_response = testing_client.delete(f'/accounts/{account_id}')
    assert delete_response.status_code == 200, (
        f"Failed to delete account. Status: {delete_response.status_code}, "
        f"Response: {delete_response.data.decode('utf-8')}"
    )

    # Verify that the account was deleted by checking the list of accounts
    get_all_response = testing_client.get('/accounts')
    assert get_all_response.status_code == 200, (
        f"Failed to get all accounts. Status: {get_all_response.status_code}, "
        f"Response: {get_all_response.data.decode('utf-8')}"
    )

    accounts_data = get_all_response.get_json()
    assert accounts_data is not None, "Get all accounts response didn't return JSON data"
    account_ids = [account['id'] for account in accounts_data.get('accounts', [])]
    assert account_id not in account_ids, "Deleted account still present in accounts list"

