class Item:

    def __init__(self, title, color, quantity, category, gender, price, manufacturer):
        self.title = title
        self.color = color
        self.quantity = int(quantity)
        self.category = category
        self.gender = gender
        self.price = float(price)
        self.manufacturer = manufacturer

    def as_args(self):
        return [self.title, self.color, self.quantity, self.category, self.gender, self.price, self.manufacturer]
