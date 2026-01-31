import pytest
from app.api import app, registry

class TestAccountTransfersAPI:

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            registry.accounts.clear()
            yield client

    @pytest.fixture
    def valid_account(self):
        return {
            "name": "alice",
            "surname": "walker",
            "pesel": "89010112345"
        }

    def test_transfer_account_not_found(self, client):
        resp = client.post('/api/accounts/00000000000/transfer', json={"amount": 100, "type": "incoming"})
        assert resp.status_code == 404

    def test_transfer_missing_fields(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"type": "incoming"})
        assert resp.status_code == 400

    def test_transfer_unknown_type_returns_400(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 100, "type": "invalid"})
        assert resp.status_code == 400

    def test_incoming_transfer_success_and_balance(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 500, "type": "incoming"})
        assert resp.status_code == 200
        r = client.get(f'/api/accounts/{valid_account["pesel"]}')
        assert r.status_code == 200
        data = r.get_json()
        assert data['balance'] == 500

    def test_outgoing_insufficient_funds_returns_422(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 100, "type": "outgoing"})
        assert resp.status_code == 422

    def test_outgoing_success(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 200, "type": "incoming"})
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 100, "type": "outgoing"})
        assert resp.status_code == 200
        r = client.get(f'/api/accounts/{valid_account["pesel"]}')
        assert r.get_json()['balance'] == 100

    def test_express_transfer_success_and_history(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 200, "type": "incoming"})
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 100, "type": "express"})
        assert resp.status_code == 200
        r = client.get(f'/api/accounts/{valid_account["pesel"]}')
        data = r.get_json()
        # fee default for personal account is 1, so balance should be 200 - 100 - 1
        assert data['balance'] == 99
        # check transaction history entries exist on the account object via registry
        acc = registry.find_account_by_pesel(valid_account['pesel'])
        assert -100 in acc.transaction_history
        assert -1 in acc.transaction_history

    def test_express_transfer_insufficient_returns_422(self, client, valid_account):
        client.post('/api/accounts', json=valid_account)
        resp = client.post(f'/api/accounts/{valid_account["pesel"]}/transfer', json={"amount": 100, "type": "express"})
        assert resp.status_code == 422
