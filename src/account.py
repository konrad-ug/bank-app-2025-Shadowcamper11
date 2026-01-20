from src.operations import Transfer_operations
import requests
from datetime import datetime
import os
try:
    from lib.smtp import SMTPClient
except Exception:
    from smtp.smtp import SMTPClient

class AccountRegistry:
    def __init__(self):
        self.accounts = []
    
    def __iter__(self):
        return iter(self.accounts)
    
    def add_account(self, account):
        # Use duck-typing to avoid issues when Account class is reloaded in tests
        if hasattr(account, 'pesel'):
            self.accounts.append(account)
            return True
        return False
        
    
    def find_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_all_accounts(self):
        return self.accounts.copy()
    
    def get_accounts_count(self):
        return len(self.accounts)


class Account(Transfer_operations):
    def __init__(self, first_name, last_name, pesel, promocode=None, fee=1):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promocode = promocode 
        self.fee = fee
        if self.is_promocode_valid(promocode) and self.is_eligible_for_promotion():
            self.balance += 50
            self.transaction_history.append(50)
        
        
        
    def is_pesel_valid(self, pesel):
        if len(pesel) == 11 and pesel.isdigit():
            return True
        return False
    
    def is_promocode_valid(self, promocode):
        if promocode is None:
            return False
        if promocode.startswith("PROM_") and len(promocode) == 8:
            return True
        return False
    
    def get_birth_year_from_pesel(self):
        
        if self.pesel == "Invalid" or len(self.pesel) != 11:
            return None
        
        year_digits = int(self.pesel[:2])
        month_digits = int(self.pesel[2:4])
        
        if 1 <= month_digits <= 12:
            return 1900 + year_digits
        elif 21 <= month_digits <= 32:
            return 2000 + year_digits
        elif 41 <= month_digits <= 52:
            return 2100 + year_digits
        elif 61 <= month_digits <= 72:
            return 2200 + year_digits
        elif 81 <= month_digits <= 92:
            return 1800 + year_digits
        else:
            return None

    def is_eligible_for_promotion(self):
        birth_year = self.get_birth_year_from_pesel()
        if birth_year is None:
            return False
        return birth_year > 1960
    
    
    def submit_for_loan(self, amount):
        if amount <= 0:
            return False
        
        if len(self.transaction_history) >= 3:
            last_three_transactions = self.transaction_history[-3:]
            if all(tx > 0 for tx in last_three_transactions):
                self.balance += amount
                self.transaction_history.append(amount)
                return True
            
        if len(self.transaction_history) >= 5:
            last_five_transactions = self.transaction_history[-5:]
            if sum(last_five_transactions) > amount:
                self.balance += amount
                self.transaction_history.append(amount)
                return True
            else: 
                return False
        
        return False
    
    def send_history_via_email(self, emial):
        today = datetime.now().strftime('%Y-%m-%d')
        subject = f"Account Transfer History {today}"
        text = f"Personal account history: {self.transaction_history}"
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, emial)

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "transaction_history": list(self.transaction_history),
        }

    @classmethod
    def from_dict(cls, data: dict):
        name = data.get('first_name') or data.get('name')
        last = data.get('last_name') or data.get('surname')
        pesel = data.get('pesel')
        acc = cls(name, last, pesel)
        acc.balance = data.get('balance', 0)
        acc.transaction_history = list(data.get('transaction_history', []))
        return acc
        
    
class Company_Account(Transfer_operations):
    def __init__(self, company_name, NIP, fee =5):
        super().__init__()
        self.company_name = company_name
        self.NIP = NIP if self.is_NIP_valid(NIP) else "Invalid"
        self.fee = fee

        if not self.validate_nip(NIP):
            raise ValueError("Company not registered!!")

    def is_NIP_valid(self, NIP):
        if len(NIP) == 10 and NIP.isdigit():
            return True
        return False
    
    
            
    def take_loan(self, amount):
        if amount <= 0:
            return False

        if self.balance < amount *2:
            return False
        if -1775 not in self.transaction_history:
            return False
        self.balance += amount
        self.transaction_history.append(amount)
        return True

    def validate_nip(self, NIP):
        base_url = os.getenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl/')
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"{base_url}api/search/nip/{NIP}?date={today}"
        
        try:
            response = requests.get(url)
            print(f"MF API Response for NIP {NIP}: {response.json()}")
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'subject' in data['result']:
                    status_vat = data['result']['subject'].get('statusVat')
                    return status_vat == 'Czynny'
            
            return False
        except Exception as e:
            print(f"Error validating NIP {NIP}: {e}")
            return False
    
    def send_history_via_email(self, emial):
        today = datetime.now().strftime('%Y-%m-%d')
        subject = f"Account Transfer History {today}"
        text = f"Company account history: {self.transaction_history}"
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, emial)

    def to_dict(self):
        return {
            "company_name": self.company_name,
            "NIP": self.NIP,
            "balance": self.balance,
            "transaction_history": list(self.transaction_history),
        }

    @classmethod
    def from_dict(cls, data: dict):
        company_name = data.get('company_name') or data.get('name')
        nip = data.get('NIP') or data.get('nip')
        acc = cls(company_name, nip)
        acc.balance = data.get('balance', 0)
        acc.transaction_history = list(data.get('transaction_history', []))
        return acc
        
            
    