from src.account import Account
from src.account import Company_Account
from src.operations import Transfer_operations


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678911")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678911"
        assert account.promocode is None
        
    def test_pesel_length(self):
        account = Account("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"
        
    def test_pesel_too_long(self):
        account = Account("John", "Doe", "123456789112")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = Account("John", "Doe", "1234567891")
        assert account.pesel == "Invalid"
    
    def test_pesel_non_numeric(self):
        account = Account("John", "Doe", "12345ABCDE1")
        assert account.pesel == "Invalid"
        
    def test_promocode_valid(self):
        account = Account("John", "Doe", "90010112345", promocode="PROM_123")
        assert account.balance == 50
    
    def test_promocode_none(self):
        account = Account("John", "Doe", "12345678911", promocode=None)
        assert account.balance == 0

    def test_promocode_invalid_format(self):
        account = Account("John", "Doe", "12345678911", promocode="PROMO123")
        assert account.balance == 0

    def test_promocode_invalid_prefix(self):
        account = Account("John", "Doe", "12345678911", promocode="INVALID_123")
        assert account.balance == 0
        
    def test_promocode_invalid_suffix(self):
        account = Account("John", "Doe", "12345678911", promocode="PROM_9992")
        assert account.balance == 0
        
    def test_promocode_valid_born_after_1960(self):
        account = Account("John", "Doe", "65010112345", promocode="PROM_123")
        assert account.balance == 50
    
    def test_promocode_valid_born_before_1960(self):
        account = Account("John", "Doe", "59010112345", promocode="PROM_123")
        assert account.balance == 0
    
    def test_promocode_valid_exactly_1960(self):
        account = Account("John", "Doe", "60010112345", promocode="PROM_123")
        assert account.balance == 0
        
    def test_birth_year_extraction_1900s(self):
        account = Account("John", "Doe", "65010112345")
        assert account.get_birth_year_from_pesel() == 1965
    
    def test_birth_year_extraction_2000s(self):
        account = Account("John", "Doe", "02210112345")
        assert account.get_birth_year_from_pesel() == 2002
    
    def test_birth_year_invalid_pesel(self):
        account = Account("John", "Doe", "12345ABCDE1")
        assert account.get_birth_year_from_pesel() is None
    
    def test_birth_year_invalid_month(self):
        account = Account("John", "Doe", "99130112345")
        assert account.get_birth_year_from_pesel() is None
    
    def test_promotion_eligibility_true(self):
        account = Account("John", "Doe", "65010112345")
        assert account.is_eligible_for_promotion() is True
        
    def test_promotion_eligibility_false(self):
        account = Account("John", "Doe", "59010112345")
        assert account.is_eligible_for_promotion() is False
    
    def test_promotion_eligibility_born_in_1960(self):
        account = Account("John", "Doe", "60010112345")
        assert account.is_eligible_for_promotion() is False
    
    def test_promotion_eligibility_invalid_pesel(self):
        account = Account("John", "Doe", "12345ABCDE1")
        assert account.is_eligible_for_promotion() is False
    

class Test_Company_Create:
    def test_company_creation(self):
        account = Company_Account("Lockhead_Martin", "1234567890")
        assert account.company_name == "Lockhead_Martin"
        assert account.NIP == "1234567890"
        assert account.balance == 0
        
    def NIP_length(self):
        account = Company_Account("Lockhead_Martin", "1234567890")
        assert account.NIP == "1234567890"
    
    def NIP_too_long(self):
        account = Company_Account("Lockhead_Martin", "12345678901")
        assert account.NIP == "Invalid"
    
    def NIP_too_short(self):
        account = Company_Account("Lockhead_Martin", "123456789")
        assert account.NIP == "Invalid"
    
    def NIP_non_numeric(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        assert account.NIP == "Invalid"
    
    def test_initial_balance(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        assert account.balance == 0
    
        
    def test_balance_incoming_transfer(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.incoming_transfer(100)
        assert account.balance == 100
    
    def test_balance_incoming_transfer(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.incoming_transfer(-100)
        assert account.balance == 0
    
    def test_balance_out_transfer(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.incoming_transfer(100)
        account.outgoing_transfer(30)
        assert account.balance == 70
    
    def test_balance_without_money_outgoing_transfer(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.incoming_transfer(20)
        account.outgoing_transfer(50)
        assert account.balance == 20
    
    def test_balance_without_money_outgoing_transfer(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.outgoing_transfer(50)
        assert account.balance == 0

    def test_balance_outgoing_with_money(self):
        account = Company_Account("Lockhead_Martin", "12345ABCDE")
        account.balance += 100
        account.outgoing_transfer(70)
        assert account.balance == 30
        
    
       