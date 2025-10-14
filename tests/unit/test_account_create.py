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
    
    def test_pesel_too_long(self):
        account = Account("John", "Doe", "1234567891")
        assert account.pesel == "Invalid"
    
    def test_pesel_non_numeric(self):
        account = Account("John", "Doe", "12345ABCDE1")
        assert account.pesel == "Invalid"
        
    def test_promocode_valid(self):
        account = Account("John", "Doe", "12345678911", promocode="PROM_123")
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