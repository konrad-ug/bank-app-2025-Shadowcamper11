import pytest
from src.account import Account, Company_Account, AccountRegistry

class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        return AccountRegistry()
    @pytest.fixture
    def account(self):
        return Account("John", "Doe", "12345678901")
    
    @pytest.fixture
    def account1(self):
        return Account("John", "Doe", "12345678911")
    
    @pytest.fixture
    def account2(self):
        return Account("Jane", "Smith", "98765432109")
    
    @pytest.fixture
    def promo_account(self):
        return Account("Alice", "Johnson", "65010112345", promocode="WELCOME_BONUS")
    
    def test_registry_create(self, registry):
        assert registry.accounts == []
        assert registry.get_accounts_count() == 0
        
    def test_add_account(self, registry, account):
        registry.add_account(account)
        assert registry.get_accounts_count() == 1
        assert registry.accounts[0] == account
    
    
    @pytest.mark.parametrize("account_count", [1, 2, 3, 6, 7, 8])
    def test_add_multiple_accounts(self, registry, account_count):
        for i in range(account_count):
            acc = Account(f"First{i}", f"Last{i}", f"{1234567891 + i}")
            registry.add_account(acc)
        assert registry.get_accounts_count() == account_count
        for acc in registry:
            assert acc in registry.accounts
    
    
    @pytest.mark.parametrize("invalid_input", ["not_an_account", 123, None, [], {},])
    def test_add_invalid_account_type(self, registry, invalid_input):
        result = registry.add_account(invalid_input)
        assert result is False
        assert registry.get_accounts_count() == 0
    
    def test_find_account_by_pesel_found(self, registry, account1, account2):
        registry.add_account(account1)
        registry.add_account(account2)
        
        found_account = registry.find_account_by_pesel("12345678911")
        assert found_account == account1
        assert found_account.first_name == "John"
        
        found_account2 = registry.find_account_by_pesel("98765432109")
        assert found_account2 == account2
        assert found_account2.first_name == "Jane"
    def test_find_account_by_pesel_not_found(self, registry, account1):
        registry.add_account(account1)
        
        found_account = registry.find_account_by_pesel("99999999999")
        assert found_account is None
    
    def test_find_account_by_pesel_empty_registry(self, registry):
        found_account = registry.find_account_by_pesel("12345678911")
        assert found_account is None
    
    @pytest.mark.parametrize("search_pesel,expected_name", [
        ("12345678911", "John"),
        ("98765432109", "Jane"),
        ("65010112345", "Alice"),
        ("00000000000", None),
    ])
    def test_find_account_scenarios(self, registry, account1, account2, promo_account, search_pesel, expected_name):
        registry.add_account(account1)
        registry.add_account(account2)
        registry.add_account(promo_account)
        
        found_account = registry.find_account_by_pesel(search_pesel)
        if expected_name:
            assert found_account is not None
            assert found_account.first_name == expected_name
        else:
            assert found_account is None
    def test_find_account_with_invalid_pesel(self, registry):
        invalid_account = Account("Invalid", "User", "invalid_pesel")
        registry.add_account(invalid_account)
        
        found_account = registry.find_account_by_pesel("Invalid")
        assert found_account == invalid_account
        assert found_account.pesel == "Invalid"
    
    def test_get_all_accounts_empty(self, registry):
        all_accounts = registry.get_all_accounts()
        assert all_accounts == []
        assert isinstance(all_accounts, list)
    
    def test_get_all_accounts_with_data(self, registry, account1, account2, promo_account):
        registry.add_account(account1)
        registry.add_account(account2)
        registry.add_account(promo_account)
        
        all_accounts = registry.get_all_accounts()
        assert len(all_accounts) == 3
        assert account1 in all_accounts
        assert account2 in all_accounts
        assert promo_account in all_accounts
        
    def test_get_all_accounts_returns_copy(self, registry, account1):
        registry.add_account(account1)
        all_accounts = registry.get_all_accounts()
        all_accounts.clear()
        assert registry.get_accounts_count() == 1
        assert account1 in registry.accounts
    
    def test_get_accounts_count_scenarios(self, registry, account1, account2):
        assert registry.get_accounts_count() == 0
        registry.add_account(account1)
        assert registry.get_accounts_count() == 1
        registry.add_account(account2)
        assert registry.get_accounts_count() == 2
    
    def test_duplicate_accounts_allowed(self, registry, account1):
        registry.add_account(account1)
        registry.add_account(account1)
        assert registry.get_accounts_count() == 2
        assert registry.accounts.count(account1) == 2
        
    
    def test_accounts_with_same_pesel(self, registry):
        account1 = Account("John", "Doe", "12345678911")
        account2 = Account("Jane", "Smith", "12345678911")
        registry.add_account(account1)
        registry.add_account(account2)
        found = registry.find_account_by_pesel("12345678911")
        assert found == account1
        assert registry.get_accounts_count() == 2
    
