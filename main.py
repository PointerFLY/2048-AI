from game import Game
from human import HumanAgent
from stochastic import StochasticAgent
from expectimax import ExpectimaxAgent
from stochastic import StochasticAgent
import sys

sys.setrecursionlimit(10000)


game = Game()
agent = ExpectimaxAgent(game)
agent.start()

game.show()
