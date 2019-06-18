class BankAccount:
    def __init__ (self,int_rate,balance=400):
        self.balance = balance
        self.int_rate = int_rate
    def deposit(self, amount):
        self.balance += amount
        return self
    def withdraw(self, amount):
        self.balance -= amount
        return self 
    def display_account_info(self):
        print(self.balance)
        return self
    def yield_interest(self):
        self.balance = self.balance + (self.balance * self.int_rate)
        return self

# first = BankAccount(.09, 200)
first = BankAccount(.09).display_account_info()
# second = BankAccount(.06, 500)

# first.deposit(50).deposit(50).deposit(50).withdraw(10).yield_interest().display_account_info()
# second.deposit(50).deposit(50).withdraw(12).withdraw(12).withdraw(12).withdraw(12).yield_interest().display_account_info()
