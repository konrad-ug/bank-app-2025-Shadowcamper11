from unittest import mock

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
