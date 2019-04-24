from game import Game
from human import HumanAgent
from stochastic import StochasticAgent
from greedy import GreedyAgent


game = Game()
agent = GreedyAgent(game)
agent.start()

game.show()
