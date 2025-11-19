from src.account import Account
from src.account import Company_Account
from src.operations import Transfer_operations
import pytest


class TestTransactions:
    
    @pytest.fixture
    def account(self):
        return Account("Jane", "Smith", "85020212345")
    
    @pytest.fixture
    def promo_account(self):
        return Account("Jane", "Smith", "85020212345", promocode="PROM_456")
    
    def test_initial_balance(self, account):
        assert account.balance == 0
    
    def test_balance_with_valid_promocode_and_eligibility(self, promo_account):
        assert promo_account.balance == 50
    
    @pytest.mark.parametrize("transfer_amount,expected_balance", [
        (100, 100),
        (250, 250),
        (0, 0),
        (-100, 0),
    ])
    def test_balance_incoming_transfer(self, account, transfer_amount, expected_balance):
        account.incoming_transfer(transfer_amount)
        assert account.balance == expected_balance
    
    @pytest.mark.parametrize("initial_amount,outgoing_amount,expected_balance", [
        (100, 30, 70),
        (100, 100, 0),
        (20, 50, 20),
        (0, 50, 0),
    ])
    def test_balance_outgoing_transfer(self, account, initial_amount, outgoing_amount, expected_balance):
        if initial_amount > 0:
            account.incoming_transfer(initial_amount)
        account.outgoing_transfer(outgoing_amount)
        assert account.balance == expected_balance
    
    def test_balance_outgoing_with_added_money(self, account):
        account.balance += 100
        account.outgoing_transfer(70)
        assert account.balance == 30