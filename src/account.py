class Account:
    def __init__(self, first_name, last_name, pesel, promocode=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promocode = promocode 
        
        if self.is_promocode_valid(promocode) and self.is_eligible_for_promotion():
            self.balance += 50
        
        
        
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