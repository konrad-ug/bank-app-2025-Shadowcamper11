class Account:
    def __init__(self, first_name, last_name, pesel, promocode=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promocode = promocode if self.is_promocode_valid(promocode) else 0.0
        
        
    def is_pesel_valid(self, pesel):
        if len(pesel) == 11 and pesel.isdigit():
            return True
        return False
    
    def is_promocode_valid(self, promocode):
        if promocode is None:
            return True
        if promocode.startswith("PROM_") and len(promocode) == 8:
            self.balance += 50
            return True
        return False