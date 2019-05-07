from game import Game
from human import HumanAgent
from stochastic import StochasticAgent
from greedy import GreedyAgent
from expectimax import ExpectimaxAgent


game = Game()
agent = ExpectimaxAgent(game)
agent.start()

game.show()
