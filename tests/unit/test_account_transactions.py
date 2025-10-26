from src.account import Account
from src.account import Company_Account
from src.operations import Transfer_operations



class TestTransactions:
    def test_initial_balance(self):
        account = Account("Jane", "Smith", "85020212345")
        assert account.balance == 0
    
    def test_balance_with_valid_promocode_and_eligibility(self):
        account = Account("Jane", "Smith", "85020212345", promocode="PROM_456")
        assert account.balance == 50
        
    def test_balance_incoming_transfer(self):
        account = Account("Jane", "Smith", "85020212345")
        account.incoming_transfer(100)
        assert account.balance == 100
    
    def test_balance_incoming_transfer(self):
        account = Account("Jane", "Smith", "85020212345")
        account.incoming_transfer(-100)
        assert account.balance == 0
    
    def test_balance_out_transfer(self):
        account = Account("Jane", "Smith", "85020212345")
        account.incoming_transfer(100)
        account.outgoing_transfer(30)
        assert account.balance == 70
    
    def test_balance_without_money_outgoing_transfer(self):
        account = Account("Jane", "Smith", "85020212345")
        account.incoming_transfer(20)
        account.outgoing_transfer(50)
        assert account.balance == 20
    
    def test_balance_without_money_outgoing_transfer(self):
        account = Account("Jane", "Smith", "85020212345")
        account.outgoing_transfer(50)
        assert account.balance == 0
    
    def test_balance_outgoing_with_monet(self):
        account = Account("Jane", "Smith", "85020212345")
        account.balance += 100
        account.outgoing_transfer(70)
        assert account.balance == 30
    
    
