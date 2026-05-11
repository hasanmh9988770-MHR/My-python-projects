class Hotel:
    def __init__(self, name, rooms, location, rating, price):
        self.name = name
        self.rooms = rooms
        self.location = location
        self.rating = rating
        self.price = price

    def book(self):
        if self.rooms > 0:
            self.rooms -= 1
            return f"Booked successfully in {self.name}"
        return "No rooms available"

    def __str__(self):
        return f"{self.name} | Rooms:{self.rooms} | {self.location} | Rating:{self.rating} | Price:{self.price}"