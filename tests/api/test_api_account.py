import pytest
from app.api import app, registry

class TestAccountCRUD:
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            registry.accounts.clear()
            yield client
    
    @pytest.fixture
    def valid_account_data(self):
        return {
            "name": "james",
            "surname": "hetfield", 
            "pesel": "89092909825"
        }
    
    @pytest.fixture
    def another_account_data(self):
        return {
            "name": "lars",
            "surname": "ulrich", 
            "pesel": "12345678901"
        }
    
    def test_get_account_by_pesel_success(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        
        assert response.status_code == 200
        account_data = response.get_json()
        assert account_data["name"] == valid_account_data["name"]
        assert account_data["surname"] == valid_account_data["surname"]
        assert account_data["pesel"] == valid_account_data["pesel"]
        assert "balance" in account_data
    
    def test_get_account_by_pesel_not_found(self, client):
        response = client.get('/api/accounts/99999999999')
        
        assert response.status_code == 404
        error_data = response.get_json()
        assert error_data["error"] == "Account not found"
    
    def test_update_account_name_only(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        update_data = {"name": "jimmy"}
        response = client.patch(f'/api/accounts/{valid_account_data["pesel"]}',
                              json=update_data,
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account updated"
        
        get_response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        updated_account = get_response.get_json()
        assert updated_account["name"] == "jimmy"
        assert updated_account["surname"] == valid_account_data["surname"]
    
    def test_update_account_surname_only(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        update_data = {"surname": "newfield"}
        response = client.patch(f'/api/accounts/{valid_account_data["pesel"]}',
                              json=update_data,
                              content_type='application/json')
        
        assert response.status_code == 200
        
        get_response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        updated_account = get_response.get_json()
        assert updated_account["name"] == valid_account_data["name"]
        assert updated_account["surname"] == "newfield"
    
    def test_update_account_both_fields(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        update_data = {"name": "kirk", "surname": "hammett"}
        response = client.patch(f'/api/accounts/{valid_account_data["pesel"]}',
                              json=update_data,
                              content_type='application/json')
        
        assert response.status_code == 200
        
        get_response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        updated_account = get_response.get_json()
        assert updated_account["name"] == "kirk"
        assert updated_account["surname"] == "hammett"
    
    def test_update_account_not_found(self, client):
        update_data = {"name": "test"}
        response = client.patch('/api/accounts/99999999999',
                              json=update_data,
                              content_type='application/json')
        
        assert response.status_code == 404
        assert response.get_json()["error"] == "Account not found"
    
    def test_update_account_no_data(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        response = client.patch(f'/api/accounts/{valid_account_data["pesel"]}',
                              json={},
                              content_type='application/json')
        
        assert response.status_code == 400
        assert response.get_json()["error"] == "No data provided"
    
    def test_delete_account_success(self, client, valid_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        
        response = client.delete(f'/api/accounts/{valid_account_data["pesel"]}')
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Account deleted"
        
        get_response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        assert get_response.status_code == 404
    
    def test_delete_account_not_found(self, client):
        response = client.delete('/api/accounts/99999999999')
        
        assert response.status_code == 404
        assert response.get_json()["error"] == "Account not found"
    
    def test_delete_account_affects_count(self, client, valid_account_data, another_account_data):
        client.post('/api/accounts', 
                   json=valid_account_data,
                   content_type='application/json')
        client.post('/api/accounts', 
                   json=another_account_data,
                   content_type='application/json')
        
        count_before = client.get('/api/accounts/count')
        initial_count = count_before.get_json()["count"]
        
        client.delete(f'/api/accounts/{valid_account_data["pesel"]}')
        
        count_after = client.get('/api/accounts/count')
        final_count = count_after.get_json()["count"]
        
        assert final_count == initial_count - 1
    
    def test_full_crud_cycle(self, client, valid_account_data):
        create_response = client.post('/api/accounts', 
                                    json=valid_account_data,
                                    content_type='application/json')
        assert create_response.status_code == 201
        
        read_response = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        assert read_response.status_code == 200
        
        update_response = client.patch(f'/api/accounts/{valid_account_data["pesel"]}',
                                     json={"name": "updated"},
                                     content_type='application/json')
        assert update_response.status_code == 200
        
        delete_response = client.delete(f'/api/accounts/{valid_account_data["pesel"]}')
        assert delete_response.status_code == 200
        
        final_read = client.get(f'/api/accounts/{valid_account_data["pesel"]}')
        assert final_read.status_code == 404