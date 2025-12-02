import pytest
from app.api import app

class TestAccountCreationAPI:
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def valid_account_data(self):
        return {
            "name": "james",
            "surname": "hetfield", 
            "pesel": "89092909825"
        }
    
    def test_create_account_success(self, client, valid_account_data):
        response = client.post('/api/accounts', 
                              json=valid_account_data,
                              content_type='application/json')
        
        assert response.status_code == 201
        response_data = response.get_json()
        assert response_data["message"] == "Account created"
    
    def test_create_account_and_verify_in_registry(self, client, valid_account_data):
        create_response = client.post('/api/accounts', 
                                     json=valid_account_data,
                                     content_type='application/json')
        assert create_response.status_code == 201
        
        get_response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        assert get_response.status_code == 200
        
        account_data = get_response.get_json()
        assert account_data["name"] == valid_account_data["name"]
        assert account_data["surname"] == valid_account_data["surname"]
        assert account_data["pesel"] == valid_account_data["pesel"]
        assert "balance" in account_data
    
    def test_create_account_missing_fields(self, client):
        invalid_data = {
            "name": "john",
            "surname": "doe"
        }
        
        response = client.post('/api/accounts', 
                              json=invalid_data,
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_get_accounts_count_after_creation(self, client, valid_account_data):
        count_before = client.get('/api/accounts/count')
        initial_count = count_before.get_json()["count"]
        
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        count_after = client.get('/api/accounts/count')
        final_count = count_after.get_json()["count"]
        
        assert final_count == initial_count + 1
    
    def test_get_all_accounts_includes_created(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        all_accounts_response = client.get('/api/accounts')
        assert all_accounts_response.status_code == 200
        
        accounts = all_accounts_response.get_json()
        
        created_account = None
        for account in accounts:
            if account["pesel"] == valid_account_data["pesel"]:
                created_account = account
                break
        
        assert created_account is not None
        assert created_account["name"] == valid_account_data["name"]
        assert created_account["surname"] == valid_account_data["surname"]
        assert created_account["balance"] == 0