class Store:
    def __init__ (self,name,products_list):
        self.name = name
        self.products_list = products_list
    def add_product(self, new_product):
        self.products_list += new_product
    # def sell_product(self,id)

class Products:
    def __init__ (self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    def update_price(self, percentage_change, is_increased):
        self.price = (self.price + percentage_change)
    def print_info(self):
        print.name().category().price()