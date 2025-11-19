from src.account import Account
from src.account import Company_Account
from src.operations import Transfer_operations
import pytest

class TestAccount:
    
    @pytest.fixture
    def account(self):
        return Account("John", "Doe", "12345678911")
    
    @pytest.fixture
    def promo_account(self):
        return Account("John", "Doe", "65010112345", promocode="PROM_123")
    
    @pytest.fixture
    def account_with_balance(self, account):
        account.incoming_transfer(1000)
        return account
    
    def test_account_creation(self, account: Account):
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678911"
        assert account.promocode is None

    @pytest.mark.parametrize("pesel,expected", [
        ("12345678911", "12345678911"),
        ("123456789112", "Invalid"),
        ("1234567891", "Invalid"),
        ("12345ABCDE1", "Invalid"),
    ])
    def test_pesel_validation(self, pesel, expected):
        account = Account("John", "Doe", pesel)
        assert account.pesel == expected

    @pytest.mark.parametrize("promocode,birth_pesel,expected_balance", [
        ("PROM_123", "90010112345", 50),
        ("PROM_123", "59010112345", 0),
        ("PROM_123", "60010112345", 0),
        (None, "12345678911", 0),
        ("PROMO123", "12345678911", 0),
        ("INVALID_123", "12345678911", 0),
        ("PROM_9992", "12345678911", 0),
    ])
    def test_promocode_scenarios(self, promocode, birth_pesel, expected_balance):
        account = Account("John", "Doe", birth_pesel, promocode=promocode)
        assert account.balance == expected_balance

    @pytest.mark.parametrize("pesel,expected_year", [
        ("65010112345", 1965),
        ("02210112345", 2002),
        ("05410112345", 2105),
        ("05610112345", 2205),
        ("05810112345", 1805),
        ("12345ABCDE1", None),
        ("99130112345", None),
    ])
    def test_birth_year_extraction(self, pesel, expected_year):
        account = Account("John", "Doe", pesel)
        assert account.get_birth_year_from_pesel() == expected_year

    @pytest.mark.parametrize("pesel,expected", [
        ("65010112345", True),
        ("59010112345", False),
        ("60010112345", False),
        ("12345ABCDE1", False),
    ])
    def test_promotion_eligibility(self, pesel, expected):
        account = Account("John", "Doe", pesel)
        assert account.is_eligible_for_promotion() is expected

    def test_account_history_empty(self, account: Account):
        assert account.transaction_history == []
    
    def test_account_history_with_promocode(self, promo_account):
        assert promo_account.transaction_history == [50.00]
        assert len(promo_account.transaction_history) == 1

    @pytest.mark.parametrize("transactions,expected_history,expected_length", [
        ([100], [100.00], 1),
        ([100, -30, 50], [100.00, -30.00, 50.00], 3),
        ([200, -50, -1], [200.00, -50.00, -1.00], 3),
        ([300, -100, -1, -50, -1], [300.00, -100.00, -1.00, -50.00, -1.00], 5),
    ])
    def test_transaction_history(self, account, transactions, expected_history, expected_length):
        for i, amount in enumerate(transactions):
            if amount > 0:
                account.incoming_transfer(amount)
            elif i > 0 and transactions[i-1] > 0 and amount == -1:
                account.express_transfer(transactions[i-1])
                break
            else:
                account.outgoing_transfer(-amount)
        assert account.transaction_history == expected_history
        assert len(account.transaction_history) == expected_length

    def test_failed_transfer_not_recorded(self, account: Account):
        account.incoming_transfer(100)
        account.outgoing_transfer(150)
        account.express_transfer(200)
        assert account.transaction_history == [100.00]
        assert len(account.transaction_history) == 1

    @pytest.mark.parametrize("loan_amount,expected_result,expected_balance", [
        (-100, False, 0),
        (0, False, 0),
    ])
    def test_loan_invalid_amount(self, account, loan_amount, expected_result, expected_balance):
        result = account.submit_for_loan(loan_amount)
        assert result is expected_result
        assert account.balance == expected_balance
        assert len(account.transaction_history) == 0

    @pytest.mark.parametrize("transactions,loan_amount,expected_result,expected_balance", [
        ([100, 200, 300], 500, True, 1100),
        ([100, 150, 200], 400, True, 850),
        ([100, -50, 200], 150, False, 250),
        ([100, 50, 200, 30, 150], 100, True, 630),
        ([100, -50, 200, -30], 100, False, 220),
        ([100, 150, 200, -50, 30], 1000, False, 430),
        ([100, -50, 200, -30, 150], 100, True, 470),
    ])
    def test_loan_scenarios(self, account, transactions, loan_amount, expected_result, expected_balance):
        for amount in transactions:
            if amount > 0:
                account.incoming_transfer(amount)
            else:
                account.outgoing_transfer(-amount)
        
        result = account.submit_for_loan(loan_amount)
        assert result is expected_result
        assert account.balance == expected_balance
        
        if expected_result:
            assert account.transaction_history[-1] == loan_amount

    def test_submit_for_loan_insufficient_history(self, account: Account):
        account.incoming_transfer(100)
        result = account.submit_for_loan(200)
        assert result is False
        assert account.balance == 100
        assert len(account.transaction_history) == 1


class TestCompanyAccount:
    
    @pytest.fixture
    def company(self):
        return Company_Account("Lockhead_Martin", "1234567890")

    def test_company_creation(self, company):
        assert company.company_name == "Lockhead_Martin"
        assert company.NIP == "1234567890"
        assert company.balance == 0

    @pytest.mark.parametrize("nip,expected", [
        ("1234567890", "1234567890"),
        ("12345678901", "Invalid"),
        ("123456789", "Invalid"),
        ("12345ABCDE", "Invalid"),
    ])
    def test_nip_validation(self, nip, expected):
        company = Company_Account("Test", nip)
        assert company.NIP == expected

    @pytest.mark.parametrize("initial_transfer,outgoing_amount,expected_balance", [
        (100, 30, 70),
        (20, 50, 20),
        (0, 50, 0),
    ])
    def test_balance_operations(self, company, initial_transfer, outgoing_amount, expected_balance):
        if initial_transfer > 0:
            company.incoming_transfer(initial_transfer)
        company.outgoing_transfer(outgoing_amount)
        assert company.balance == expected_balance

    def test_balance_incoming_transfer_negative(self, company):
        company.incoming_transfer(-100)
        assert company.balance == 0

    def test_balance_outgoing_with_added_money(self, company):
        company.balance += 100
        company.outgoing_transfer(70)
        assert company.balance == 30

    def test_company_history_empty(self, company):
        assert company.transaction_history == []

    @pytest.mark.parametrize("transactions,expected_history,expected_length", [
        ([100], [100.00], 1),
        ([100, -30, 50], [100.00, -30.00, 50.00], 3),
        ([200, -50, -5], [200.00, -50.00, -5.00], 3),
        ([300, -100, -5, -50, -5], [300.00, -100.00, -5.00, -50.00, -5.00], 5),
    ])
    def test_company_transaction_history(self, company, transactions, expected_history, expected_length):
        i = 0
        while i < len(transactions):
            amount = transactions[i]
        
            if amount > 0:
                company.incoming_transfer(amount)
                i += 1
            elif amount == -5:
                prev_amount = None
                j = i - 1
                while j >= 0:
                    if transactions[j] < 0 and transactions[j] != -5:
                        prev_amount = -transactions[j]
                        break
                    j -= 1
            
                if prev_amount:
                    company.express_transfer(prev_amount)
                i += 1
            elif amount < 0 and amount != -5:
                if i + 1 < len(transactions) and transactions[i + 1] == -5:
                    i += 1
                else:
                    company.outgoing_transfer(-amount)
                    i += 1
            else:
                i += 1
            
        assert company.transaction_history == expected_history
        assert len(company.transaction_history) == expected_length

    def test_company_failed_transfer_not_recorded(self, company):
        company.incoming_transfer(100)
        company.outgoing_transfer(150)
        company.express_transfer(200)
        assert company.transaction_history == [100.00]
        assert len(company.transaction_history) == 1
 
    @pytest.mark.parametrize("loan_amount,expected_result,expected_balance", [
        (-100, False, 0),
        (0, False, 0),
    ])
    def test_take_loan_invalid_amount(self, company, loan_amount, expected_result, expected_balance):
        company.incoming_transfer(5000)
        company.outgoing_transfer(1775)
        result = company.take_loan(loan_amount)
        assert result is expected_result
        assert company.balance == 3225

    @pytest.mark.parametrize("balance,has_zus,loan_amount,expected_result", [
        (10000, True, 4000, True),    # 8225 >= 8000
        (10000, True, 5000, False),   # 8225 < 10000
        (6000, True, 2000, True),     # 4225 >= 4000
        (6000, False, 2000, False),   # Brak ZUS 
        (4000, True, 1000, True),     # 2225 >= 2000 
        (3000, True, 1000, False),    # 1225 < 2000
        (8000, True, 4000, False),    # 6225 < 8000
        (10000, False, 1000, False),  # Brak ZUS
    ])
    def test_take_loan_scenarios(self, company, balance, has_zus, loan_amount, expected_result):
        company.incoming_transfer(balance)
        if has_zus:
            company.outgoing_transfer(1775)  # ZUS
        else:
            company.outgoing_transfer(500)   # Inny przelew
        
        initial_balance = company.balance
        result = company.take_loan(loan_amount)
        
        assert result is expected_result
        if expected_result:
            assert company.balance == initial_balance + loan_amount
            assert company.transaction_history[-1] == loan_amount
        else:
            assert company.balance == initial_balance
            assert loan_amount not in company.transaction_history

    @pytest.mark.parametrize("zus_transfers,other_transfers,loan_amount,expected_result", [
        ([1775], [], 2000, True),           # Jeden ZUS
        ([1775, 1775], [], 3000, True),     # Dwa ZUS
        ([], [1000, 500], 1000, False),     # Brak ZUS
        ([1775], [500, 200], 2000, True),   # ZUS + inne
        ([1700], [], 1000, False),          # Prawie ZUS
        ([1775, 1700], [], 2000, True),     # ZUS + prawie ZUS
    ])
    def test_take_loan_zus_variations(self, company, zus_transfers, other_transfers, loan_amount, expected_result):
        company.incoming_transfer(10000)
        
        for amount in zus_transfers + other_transfers:
            company.outgoing_transfer(amount)
        
        initial_balance = company.balance
        result = company.take_loan(loan_amount)
        
        assert result is expected_result
        if expected_result:
            assert company.balance == initial_balance + loan_amount
        else:
            assert company.balance == initial_balance

    @pytest.mark.parametrize("setup_balance,setup_zus,exact_multiplier", [
        (5000, True, 2.0),   # Dokładnie 2x
        (6000, True, 2.5),   # Więcej niż 2x  
        (4500, True, 1.9),   # Mniej niż 2x
    ])
    def test_take_loan_balance_edge_cases(self, company, setup_balance, setup_zus, exact_multiplier):
        company.incoming_transfer(setup_balance)
        if setup_zus:
            company.outgoing_transfer(1775)
        
        current_balance = company.balance
        loan_amount = int(current_balance / exact_multiplier)
        
        result = company.take_loan(loan_amount)
        expected_result = setup_zus and (current_balance >= 2 * loan_amount)
        
        assert result is expected_result

    def test_take_loan_with_express_zus(self, company):
        company.incoming_transfer(10000)
        company.express_transfer(1775)  # ZUS przez express
        
        result = company.take_loan(4000)  # 8220 >= 8000
        assert result is True
        assert company.balance == 12220  # 8220 + 4000
        assert -1775 in company.transaction_history
        assert -5 in company.transaction_history

    def test_take_loan_multiple_attempts(self, company):
        company.incoming_transfer(10000)
        company.outgoing_transfer(1775)  # ZUS
        
        result1 = company.take_loan(2000)  # 8225 >= 4000 
        assert result1 is True
        assert company.balance == 10225
        
        result2 = company.take_loan(6000)  # 10225 < 12000 
        assert result2 is False
        assert company.balance == 10225  # Bez zmian

    @pytest.mark.parametrize("mixed_operations", [
        ([("incoming", 8000), ("outgoing", 1775), ("express", 500)]),
        ([("incoming", 10000), ("express", 1775), ("incoming", 2000)]),
        ([("incoming", 5000), ("outgoing", 500), ("outgoing", 1775), ("incoming", 3000)]),
    ])
    def test_take_loan_mixed_operations(self, company, mixed_operations):
        for operation, amount in mixed_operations:
            if operation == "incoming":
                company.incoming_transfer(amount)
            elif operation == "outgoing":
                company.outgoing_transfer(amount)
            elif operation == "express":
                company.express_transfer(amount)
        
        has_zus = -1775 in company.transaction_history
        current_balance = company.balance
        loan_amount = 2000
        
        result = company.take_loan(loan_amount)
        expected_result = has_zus and (current_balance >= 2 * loan_amount)
        
        assert result is expected_result
