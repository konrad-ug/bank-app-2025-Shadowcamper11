from typing import List
import os
import pymongo
from src.account import Account, Company_Account


class AccountsRepository:
    def save_all(self, accounts: List[Account]):
        raise NotImplementedError()

    def load_all(self) -> List[Account]:
        raise NotImplementedError()


class MongoAccountsRepository(AccountsRepository):
    def __init__(self, collection):
        self._collection = collection

    def save_all(self, accounts: List[Account]):
        self._collection.delete_many({})
        for account in accounts:
            data = None
            if isinstance(account, Company_Account):
                data = account.to_dict()
                selector = {"NIP": data.get("NIP")}
            else:
                data = account.to_dict()
                selector = {"pesel": data.get("pesel")}

            self._collection.update_one(selector, {"$set": data}, upsert=True)

    def load_all(self) -> List[Account]:
        results = []
        for doc in self._collection.find():
            if 'pesel' in doc:
                results.append(Account.from_dict(doc))
            elif 'NIP' in doc or 'nip' in doc:
                results.append(Company_Account.from_dict(doc))
        return results


def create_mongo_repo_from_env():
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = pymongo.MongoClient(mongo_url)
    db_name = os.environ.get('MONGO_DB', 'bank_app')
    col_name = os.environ.get('MONGO_COLLECTION', 'accounts')
    db = client[db_name]
    collection = db[col_name]
    return MongoAccountsRepository(collection)
