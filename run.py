import sys

import click
from dotenv import load_dotenv

from game2048.agents.expectimax import ExpectimaxAgent
from game2048.agents.llm import LLMAgent
from game2048.agents.montecarlo import (
    HybridAgent,
    MonteCarloAgent,
    SmartMonteCarloAgent,
)
from game2048.core.game import Game


def create_agent(agent_name: str, game: Game, **kwargs):
    """
    Creates and returns the specified agent.

    Args:
        agent_name: Name of the agent to create
        game: Game instance to pass to the agent

    Returns:
        Agent instance
    """
    agents = {
        "llm": LLMAgent,
        "expectimax": ExpectimaxAgent,
        "montecarlo": MonteCarloAgent,
        "hybrid": HybridAgent,
        "smart_montecarlo": SmartMonteCarloAgent,
    }

    if agent_name not in agents:
        raise ValueError(
            f"Unknown agent: {agent_name}. Valid agents are: {', '.join(agents.keys())}"
        )

    if agent_name == "llm":
        return agents[agent_name](game, api_key=kwargs.get("api_key"))

    return agents[agent_name](game)


@click.command(help="Play 2048 game with different AI agents")
@click.option(
    "--agent",
    "-a",
    type=click.Choice(
        ["llm", "expectimax", "montecarlo", "hybrid", "smart_montecarlo"],
        case_sensitive=False,
    ),
    default="expectimax",
    help="Agent to use for playing the game",
)
@click.option(
    "--api-key",
    envvar="GEMINI_API_KEY",
    help="Gemini API key for LLM agent. Can also be set via GEMINI_API_KEY env var.",
)
def main(agent: str, api_key: str):
    # Increase recursion limit for expectimax
    sys.setrecursionlimit(10000)

    # Create game and agent
    game = Game()
    agent_instance = create_agent(agent, game, api_key=api_key)

    # Start the game
    agent_instance.start()
    game.show()


if __name__ == "__main__":
    # Load environment variables from .env file before running the CLI
    load_dotenv()
    main()
