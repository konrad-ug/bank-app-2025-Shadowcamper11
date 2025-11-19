from src.account import Account
from src.account import Company_Account
from src.operations import Transfer_operations
import pytest


class TestExpressTransfer:
    
    @pytest.fixture
    def individual_account(self):
        return Account("John", "Doe", "65010112345")
    
    @pytest.fixture
    def company_account(self):
        return Company_Account("Lockhead_Martin", "12345ABCDE")
    
    @pytest.mark.parametrize("account_type,initial_balance,transfer_amount,expected_balance,expected_fee", [
        ("individual", 200, 100, 99, 1),
        ("company", 200, 100, 95, 5),
    ])
    def test_express_transfer_fee(self, individual_account, company_account, account_type, initial_balance, transfer_amount, expected_balance, expected_fee):
        account = individual_account if account_type == "individual" else company_account
        account.balance += initial_balance
        account.express_transfer(transfer_amount)
        assert account.balance == expected_balance
        assert account.fee == expected_fee
    
    @pytest.mark.parametrize("account_type,initial_balance,transfer_amount,expected_balance", [
        ("individual", 100, 200, 100),
        ("company", 100, 200, 100),
    ])
    def test_express_transfer_insufficient_funds(self, individual_account, company_account, account_type, initial_balance, transfer_amount, expected_balance):
        account = individual_account if account_type == "individual" else company_account
        account.balance += initial_balance
        account.express_transfer(transfer_amount)
        assert account.balance == expected_balance
    
    @pytest.mark.parametrize("account_type,initial_balance,transfer_amount,expected_balance", [
        ("individual", 100, 100, -1),
        ("company", 100, 100, -5),
    ])
    def test_express_transfer_on_limit(self, individual_account, company_account, account_type, initial_balance, transfer_amount, expected_balance):
        account = individual_account if account_type == "individual" else company_account
        account.balance += initial_balance
        account.express_transfer(transfer_amount)
        assert account.balance == expected_balance