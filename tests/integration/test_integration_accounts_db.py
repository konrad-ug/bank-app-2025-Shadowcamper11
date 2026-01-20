import os

import pytest
from pymongo import MongoClient

from app.api import app, registry
from src.account import Account


def mongo_client_or_skip():
    url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    try:
        client = MongoClient(url, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        return client
    except Exception as e:
        pytest.skip(f"Mongo not available at {url}: {e}")


def test_save_and_load_end_to_end():
    mongo_client = mongo_client_or_skip()
    db_name = os.environ.get('MONGO_DB', 'bank_app')
    coll_name = os.environ.get('MONGO_COLLECTION', 'accounts')
    db = mongo_client[db_name]
    coll = db[coll_name]
    coll.delete_many({})
    registry.accounts.clear()
    registry.add_account(Account('Integration', 'Tester', '77777777777'))

    app.testing = True
    with app.test_client() as client_app:
        rv = client_app.post('/api/accounts/save')
        assert rv.status_code == 200

        registry.accounts.clear()
        assert registry.get_accounts_count() == 0

        rv2 = client_app.post('/api/accounts/load')
        assert rv2.status_code == 200
        assert registry.get_accounts_count() == 1
    coll.delete_many({})
