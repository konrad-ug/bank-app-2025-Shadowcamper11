from src.account import Account


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
    
    