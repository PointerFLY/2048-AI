from game import Game
from human import HumanAgent


game = Game()
agent = HumanAgent(game)
agent.start()

game.show()
