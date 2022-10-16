class Unit:
    def __init__(self, ap, available):
        self.ap = ap
        self.availabe = available

class Legionary(Unit):
    def __init__(self, ap, available = False):
        super(Legionary, self).__init__(self, ap)


if __name__ == "__main__":
    u = Unit()
    print(u.__dict__)