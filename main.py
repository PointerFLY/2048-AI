from game import Game
from human import HumanAgent
from stochastic import StochasticAgent
from greedy import GreedyAgent
from expectimax import ExpectimaxAgent
# from learning import LearningAgent
import sys

sys.setrecursionlimit(10000)


game = Game()
agent = ExpectimaxAgent(game)
agent.start()

game.show()
