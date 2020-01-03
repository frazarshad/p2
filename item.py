class Item:

    def __init__(self, serial, title, date_added, color, quantity, category, gender, price, manufacturer):
        self.serial = serial
        self.title = title
        self.date_added = date_added
        self.color = color
        self.quantity = int(quantity)
        self.category = category
        self.gender = gender
        self.price = float(price)
        self.manufacturer = manufacturer

    def as_args(self):
        return [self.title, self.color, self.quantity, self.category, self.gender, self.price, self.manufacturer]
