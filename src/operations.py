class Transfer_operations:
    def __init__(self):
        self.balance = 0
        self.fee = 0
        

    def incoming_transfer(self, amount):
        if amount > 0 and amount:
            self.balance += amount
            return True
        return False
            
    def outgoing_transfer(self, amount):
        if amount > self.balance or amount < 0:
            return False
        else:
            self.balance -= amount
            return True
    
    def express_transfer(self, amount):
        if amount > self.balance + self.fee or amount < 0:
            return False

        self.balance -= (amount + self.fee)
        return True
