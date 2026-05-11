class User:
    def __init__(self, name, uid, cost):
        self.name = name
        self.uid = uid
        self.cost = cost

    def __str__(self):
        return f"{self.name} | ID:{self.uid} | Cost:{self.cost}"