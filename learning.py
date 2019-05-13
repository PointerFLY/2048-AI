from agent import Agent
from state import State
import tensorflow as tf
import numpy as np


class LearningAgent(Agent):
    def __init__(self, game):
        super(LearningAgent, self).__init__(game)

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer((16,)))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(4, activation='softmax'))
        model.compile(optimizer=tf.train.AdamOptimizer(0.001),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        self.model = model

    def next_action(self):
        legal_actions = self.state.legal_actions()
        if not legal_actions:
            return None

        matrix = tf.cast(self.state.matrix, dtype=tf.float32)
        input_tensor = tf.reshape(matrix, [1, 16])
        result = self.model.predict(input_tensor, steps=1)[0]

        max_index = max(list(range(len(legal_actions))), key=lambda x: result[x])

        return legal_actions[max_index]
