from game import Game
from stochastic import StochasticAgent
from expectimax import ExpectimaxAgent
from monte_carlo import MonteCarloAgent
from mcts import MonteCarloTreeSearchAgent
import argparse
import sys


def create_agent(agent_name: str, game: Game):
    """
    Creates and returns the specified agent.

    Args:
        agent_name: Name of the agent to create
        game: Game instance to pass to the agent

    Returns:
        Agent instance
    """
    agents = {
        "stochastic": StochasticAgent,
        "expectimax": ExpectimaxAgent,
        "monte_carlo": MonteCarloAgent,
        "mcts": MonteCarloTreeSearchAgent,
    }

    if agent_name not in agents:
        raise ValueError(
            f"Unknown agent: {agent_name}. Valid agents are: {', '.join(agents.keys())}"
        )

    return agents[agent_name](game)


def main():
    # Increase recursion limit for expectimax
    sys.setrecursionlimit(10000)

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Play game with different AI agents")
    parser.add_argument(
        "--agent",
        "-a",
        choices=["stochastic", "expectimax", "monte_carlo", "mcts"],
        default="expectimax",
        help="Agent to use for playing the game",
    )

    args = parser.parse_args()

    # Create game and agent
    game = Game()
    agent = create_agent(args.agent, game)

    # Start the game
    agent.start()
    game.show()


if __name__ == "__main__":
    main()
