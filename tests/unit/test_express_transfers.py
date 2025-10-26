from src.account import Account
from src.account import Company_Account
from src.operations import Transfer_operations

class Test_Express_Transfer:
    def test_express_transfer_fee_company(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.balance += 200
        account.express_transfer(100)
        assert account.balance == 95
    
    def test_express_transfer_fee_individual(self):
        account = Account("John", "Doe", "65010112345")
        account.balance += 200
        account.express_transfer(100)
        assert account.balance == 99
    
    def test_express_transfer_insufficient_funds_company(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.balance += 100
        account.express_transfer(200)
        assert account.balance == 100
    
    def test_express_transfer_on_limit_company(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.balance += 100
        account.express_transfer(100)
        assert account.balance == -5
    
    def test_express_transfer_insufficient_funds_individual(self):
        account = Account("John", "Doe", "65010112345")
        account.balance += 100
        account.express_transfer(200)
        assert account.balance == 100
    
    def test_express_transfer_on_limit_individual(self):
        account = Account("John", "Doe", "65010112345")
        account.balance += 100
        account.express_transfer(100)
        assert account.balance == -1
 