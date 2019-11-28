from game import Game
from human import HumanAgent
from stochastic import StochasticAgent
from expectimax import ExpectimaxAgent
from stochastic import StochasticAgent
from monte_carlo import MonteCarloAgent
from mcts import MonteCarloTreeSearchAgent
import sys

sys.setrecursionlimit(10000)


game = Game()
agent = MonteCarloTreeSearchAgent(game)
agent.start()

game.show()
