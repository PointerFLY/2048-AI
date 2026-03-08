import random

from google import genai
from google.genai import types

from game2048.agents.agent import Agent


class LLMAgent(Agent):
    def __init__(self, state):
        super().__init__(state)
        # Assumes GEMINI_API_KEY is set in the environment
        self.client = genai.Client()
        self.model = "gemini-2.5-flash"

    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        prompt = (
            "You are an expert AI player of the game 2048.\n"
            "The goal of the game is to slide numbered tiles on a grid to "
            "combine them to create a tile with the number 2048 or higher.\n"
            "Rules:\n"
            "- You can move tiles in four directions: up, down, left, right.\n"
            "- When two tiles with the same number touch, they merge into one "
            "tile with double the value.\n"
            "- After every move, a new tile (2 or 4) appears in a random empty "
            "spot.\n\n"
            "Winning Strategy:\n"
            "- Keep your highest value tile in one of the corners.\n"
            "- Build a 'monotonic sequence' (tiles decreasing in value) leading "
            "away from your highest tile.\n"
            "- Avoid moving the highest tile out of its corner.\n"
            "- Keep the row or column with the highest tile full so it doesn't "
            "accidentally move.\n\n"
            "Current board state (0 represents an empty tile):\n"
        )
        for row in self.state.matrix:
            prompt += f"{row}\n"

        prompt += f"\nLegal actions available: {', '.join(legal_actions)}\n"
        prompt += (
            "Based on the board state, strategy, and legal actions, choose the "
            "single best move.\n"
            "Output ONLY the exact action name from the legal actions list, "
            "with no formatting, punctuation, or explanation."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0,
                ),
            )

            text = response.text.strip().lower()

            for action in legal_actions:
                if action in text:
                    return action

        except Exception as e:
            print(f"LLM Agent encountered an error: {e}")

        # Fallback to random legal action if LLM fails or outputs invalid action
        idx = random.randrange(len(legal_actions))
        return legal_actions[idx]
