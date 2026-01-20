from unittest import mock
import types
import pytest

from src.accounts_repository import MongoAccountsRepository
from src.account import Account, Company_Account


def test_save_all_calls_collection_methods():
    acc1 = Account('Jan', 'Kowalski', '11111111111')
    acc2 = Account('Anna', 'Nowak', '22222222222')

    mock_collection = mock.Mock()
    repo = MongoAccountsRepository(mock_collection)

    repo.save_all([acc1, acc2])

    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.call_count == 2


def test_load_all_returns_accounts():
    acc1 = Account('A', 'B', '33333333333')
    acc2 = Account('C', 'D', '44444444444')
    d1 = acc1.to_dict()
    d2 = acc2.to_dict()

    mock_collection = mock.Mock()
    mock_collection.find.return_value = [d1, d2]

    repo = MongoAccountsRepository(mock_collection)
    loaded = repo.load_all()

    assert len(loaded) == 2
    assert loaded[0].pesel == d1['pesel']


def test_accounts_repository_abstract_methods_raise():
    from src.accounts_repository import AccountsRepository
    r = AccountsRepository()
    with pytest.raises(NotImplementedError):
        r.save_all([])
    with pytest.raises(NotImplementedError):
        r.load_all()


def test_create_mongo_repo_from_env_monkeypatch(monkeypatch):
    import src.accounts_repository as repo_mod

    class DummyCollection:
        pass

    class DummyDB(dict):
        def __getitem__(self, name):
            return DummyCollection()

    class DummyClient(dict):
        def __init__(self, url):
            self.url = url
        def __getitem__(self, name):
            return DummyDB()

    monkeypatch.setattr(repo_mod, 'pymongo', types.SimpleNamespace(MongoClient=lambda url: DummyClient(url)))

    repo = repo_mod.create_mongo_repo_from_env()
    assert isinstance(repo, MongoAccountsRepository)
    assert hasattr(repo, '_collection')


def test_save_all_company_selector():
    mock_collection = mock.Mock()

    # create a Company_Account-like object without running its constructor
    comp = Company_Account.__new__(Company_Account)
    comp.company_name = 'C'
    comp.NIP = '1234567890'
    def to_dict():
        return {"company_name": comp.company_name, "NIP": comp.NIP, "balance": 0, "transaction_history": []}
    comp.to_dict = to_dict

    repo = MongoAccountsRepository(mock_collection)
    repo.save_all([comp])

    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.update_one.assert_called_once()
    args, kwargs = mock_collection.update_one.call_args
    assert args[0] == {"NIP": comp.NIP}


def test_load_all_calls_from_dicts(monkeypatch):
    mock_collection = mock.Mock()
    docs = [
        {"pesel": "11111111111", "first_name": "A"},
        {"NIP": "2222222222", "company_name": "B"}
    ]
    mock_collection.find.return_value = docs

    import src.accounts_repository as ar
    monkeypatch.setattr(ar, 'Account', mock.Mock(from_dict=lambda d: 'acc_obj'))
    monkeypatch.setattr(ar, 'Company_Account', mock.Mock(from_dict=lambda d: 'comp_obj'))

    repo = MongoAccountsRepository(mock_collection)
    loaded = repo.load_all()
    assert loaded == ['acc_obj', 'comp_obj']
