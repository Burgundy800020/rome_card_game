from random import randint, choices
import Card

class GameManager:
    players = []
    dpile = []
    
    def __init__(self):
        pass

    def generateCard(self, n):
        return [card(randint(1, 6)) for card in choices(Card.cards, weights=list(range(10, 0, -1)), k=n)]

if __name__ == "__main__":
    g = GameManager()
    print(g.generateCard(10))