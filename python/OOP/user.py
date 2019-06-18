class User:	
    def __init__(self, username, email_address):
        self.name = username
        self.email = email_address
        self.account = BankAccount (int_rate=0.02, balance=0)
    def make_deposit(self,amount):
        self.account += amount
        return self
    def make_withdrawl(self,amount):
        self.account -= amount
        return self
    def display_user_balance(self):
        print(self.account)
        return self


guido = User("Guido van Rossum", "guido@python.com")
monty = User("Monty Python", "monty@python.com")
roois = User("Roois", "herro@herro.com")
# guido.make_deposit(100).make_deposit(300).make_deposit(200).make_withdrawl(50).display_user_balance()
# monty.make_withdrawl(50).make_withdrawl(220).display_user_balance()
# roois.make_deposit(20000).make_withdrawl(100).make_withdrawl(300).make_withdrawl(500).display_user_balance()

roois.account().display_user_balance()