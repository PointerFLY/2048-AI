import math
import time
from random import randrange

from game2048.agents.agent import Agent


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.value = 0.0
        # Make a copy so we do not mutate the state's cache
        self.untried_actions = list(state.legal_actions())

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_terminal(self):
        return len(self.state.legal_actions()) == 0

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.copy()
        next_state.perform_action(action)
        child_node = Node(next_state, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    def best_child(self, exploration_weight=1000.0):
        best_value = -float("inf")
        best_nodes = []
        for child in self.children:
            if child.visits == 0:
                uct_value = float("inf")
            else:
                # UCT formula
                exploitation = child.value / child.visits
                exploration = exploration_weight * math.sqrt(
                    math.log(self.visits) / child.visits
                )
                uct_value = exploitation + exploration

            if uct_value > best_value:
                best_value = uct_value
                best_nodes = [child]
            elif uct_value == best_value:
                best_nodes.append(child)

        return best_nodes[randrange(len(best_nodes))]


class MCTSAgent(Agent):
    def __init__(self, game):
        super().__init__(game)
        self.time_limit = 0.25  # seconds per move

    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        # Root node of the search tree
        root = Node(self.state.copy())
        start_time = time.time()

        # Run MCTS until we run out of time
        while time.time() - start_time < self.time_limit:
            node = self._tree_policy(root)
            reward = self._default_policy(node.state)
            self._backpropagate(node, reward)

        # Return the best action found (with 0 exploration to pick
        # strictly the best avg score)
        best_node = root.best_child(exploration_weight=0.0)
        return best_node.action

    def _tree_policy(self, node):
        """Select or expand a node to simulate from."""
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.best_child()
        return node

    def _default_policy(self, state):
        """Random rollout from the current state to the end of the game."""
        current_state = state.copy()
        while True:
            legal_actions = current_state.legal_actions()
            if not legal_actions:
                break
            action = legal_actions[randrange(len(legal_actions))]
            current_state.perform_action(action)
        return current_state.score

    def _backpropagate(self, node, reward):
        """Propagate the reward up the tree."""
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent
