class Transfer_operations:
    def __init__(self):
        self.balance = 0
        self.fee = 0
        self.transaction_history = []
        

    def incoming_transfer(self, amount):
        if amount > 0 and amount:
            self.balance += amount
            self.transaction_history.append(amount)
            return True
        return False
            
    def outgoing_transfer(self, amount):
        if amount > self.balance or amount < 0:
            return False
        else:
            self.balance -= amount
            self.transaction_history.append(-amount)
            return True
    
    def express_transfer(self, amount):
        if amount > self.balance + self.fee or amount < 0:
            return False

        self.balance -= (amount + self.fee)
        self.transaction_history.append(-amount)
        self.transaction_history.append(-self.fee)
        return True
