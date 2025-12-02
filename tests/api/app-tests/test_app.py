import pytest
from app.api import app, registry

class TestAccountAPI:
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            registry.accounts.clear()
            yield client
    
    @pytest.fixture
    def test_account_data(self):
        return {
            "name": "testuser",
            "surname": "testlast", 
            "pesel": "11111111111"
        }
    
    def test_get_account_by_pesel_success(self, client, test_account_data):
        client.post('/api/accounts', 
                   json=test_account_data,
                   content_type='application/json')
        
        response = client.get(f'/api/accounts/{test_account_data["pesel"]}')
        
        assert response.status_code == 200
        account_data = response.get_json()
        assert account_data["name"] == test_account_data["name"]
        assert account_data["surname"] == test_account_data["surname"]
        assert account_data["pesel"] == test_account_data["pesel"]
        assert "balance" in account_data
    
    def test_get_account_by_pesel_not_found(self, client):
        response = client.get('/api/accounts/00000000000')
        
        assert response.status_code == 404
        error_data = response.get_json()
        assert error_data["error"] == "Account not found"
    
    def test_update_account_patch(self, client, test_account_data):
        client.post('/api/accounts', 
                   json=test_account_data,
                   content_type='application/json')
        
        update_data = {"name": "newname", "surname": "newsurname"}
        response = client.patch(f'/api/accounts/{test_account_data["pesel"]}',
                               json=update_data,
                               content_type='application/json')
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account updated"
        
        get_response = client.get(f'/api/accounts/{test_account_data["pesel"]}')
        updated_account = get_response.get_json()
        assert updated_account["name"] == "newname"
        assert updated_account["surname"] == "newsurname"
    
    def test_update_account_partial(self, client, test_account_data):
        client.post('/api/accounts', 
                   json=test_account_data,
                   content_type='application/json')
        
        update_data = {"name": "onlyname"}
        response = client.patch(f'/api/accounts/{test_account_data["pesel"]}',
                               json=update_data,
                               content_type='application/json')
        
        assert response.status_code == 200
        
        get_response = client.get(f'/api/accounts/{test_account_data["pesel"]}')
        updated_account = get_response.get_json()
        assert updated_account["name"] == "onlyname"
        assert updated_account["surname"] == test_account_data["surname"]
    
    def test_delete_account_success(self, client, test_account_data):
        client.post('/api/accounts', 
                   json=test_account_data,
                   content_type='application/json')
        
        response = client.delete(f'/api/accounts/{test_account_data["pesel"]}')
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account deleted"
        
        get_response = client.get(f'/api/accounts/{test_account_data["pesel"]}')
        assert get_response.status_code == 404
    
    def test_delete_account_not_found(self, client):
        response = client.delete('/api/accounts/00000000000')
        
        assert response.status_code == 404
        assert response.get_json()["error"] == "Account not found"
    
    def test_update_account_not_found(self, client):
        update_data = {"name": "test"}
        response = client.patch('/api/accounts/00000000000',
                               json=update_data,
                               content_type='application/json')
        
        assert response.status_code == 404
        assert response.get_json()["error"] == "Account not found"