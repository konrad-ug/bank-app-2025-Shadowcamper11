from unittest import mock

import pytest

from app.api import app, registry
from src.account import Account


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_save_endpoint_calls_repository(monkeypatch, client):
    mock_repo = mock.Mock()
    monkeypatch.setattr('app.api.create_mongo_repo_from_env', lambda: mock_repo)

    registry.accounts.clear()
    registry.add_account(Account('Piotr', 'Z', '55555555555'))

    rv = client.post('/api/accounts/save')
    assert rv.status_code == 200
    mock_repo.save_all.assert_called_once()


def test_load_endpoint_replaces_registry(monkeypatch, client):
    loaded_acc = Account('Loaded', 'User', '99999999999')
    mock_repo = mock.Mock()
    mock_repo.load_all.return_value = [loaded_acc]
    monkeypatch.setattr('app.api.create_mongo_repo_from_env', lambda: mock_repo)

    registry.accounts.clear()

    rv = client.post('/api/accounts/load')
    assert rv.status_code == 200
    assert registry.get_accounts_count() == 1
    assert registry.find_account_by_pesel('99999999999') is not None
