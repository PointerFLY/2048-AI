from agent import Agent
from state import State, Action
from random import randrange
import math
from typing import Set, List, Optional

_ITER_COUNT = 1000


class TreeNode:
    def __init__(self, state: State):
        self.parent: Optional[TreeNode] = None
        self.state = state
        self.from_action: Optional[Action] = None
        self.children: List[TreeNode] = []
        self.num_visited = 0
        self.total_score = 0


class MonteCarloTreeSearchAgent(Agent):
    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        root = TreeNode(self.state)
        for _ in range(_ITER_COUNT):
            self.search(root)

        best_action = max(root.children, key=lambda x: x.quality).from_action

        return best_action

    def search(self, node):
        node.num_visited += 1
        legal_actions = node.state.legal_actions()

        if not legal_actions:
            self.back_propagate(node, node.state.score)
        elif len(legal_actions) == node.children:
            next_node = self.rollout(node)
            self.search(next_node)
        else:
            action_set = set(legal_actions)
            for child in node.children:
                if child.from_action in action_set:
                    action_set.remove(child.from_action)
            action = action_set.pop()

            child = TreeNode(node.state.direct_successor(action))
            child.from_action = action
            child.parent = node
            node.children.append(child)

            score = self.simulate(child)
            child.num_visited = 1
            child.total_score = score
            self.back_propagate(child, score)

    def rollout(self, node: TreeNode) -> TreeNode:
        def ucb(node: TreeNode):
            quality = node.total_score / node.num_visited
            c = math.sqrt(2)
            explore = math.sqrt(math.log2(node.parent.num_visited) / node.num_visited)
            return quality + c * explore

        return max(node.children, key=ucb)

    def back_propagate(self, node: TreeNode, score):
        parent = node.parent
        while parent:
            parent.total_score += score
            parent = node.parent

    def simulate(self, node):
        state = node.state.copy()
        legal_actions = state.legal_actions()
        while legal_actions:
            idx = randrange(len(legal_actions))
            act = legal_actions[idx]
            state.perform_action(act)
            legal_actions = state.legal_actions()

        return state.score