from agent import Agent
from state import State, Action
from typing import Set, List, Optional
from game import Game
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np


class DNNAgent(Agent):
    def __init__(self, game: Game):
        super(DNNAgent, self).__init__(game)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = Net().to(self.device)

    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return

        def get_score(action) -> int:
            new_state = self.state.direct_successor(action)
            old_vec = torch.from_numpy(np.array(self.state.matrix, "float32").flatten()).to(self.device)
            new_vec = torch.from_numpy(np.array(new_state.matrix, "float32").flatten()).to(self.device)
            return self.model(new_vec) - self.model(old_vec)

        best_action = max(legal_actions, key=get_score)
        return best_action


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(in_features=4 * 4, out_features=256)
        self.fc2 = nn.Linear(in_features=256, out_features=256)
        self.fc3 = nn.Linear(in_features=256, out_features=256)
        self.fc4 = nn.Linear(in_features=256, out_features=1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)

        return x


