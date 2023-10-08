import numpy as np


class NeuralNetwork():

    def __init__(self, layer_sizes):
        self.W1 = np.random.randn(layer_sizes[0], layer_sizes[1])
        self.W2 = np.random.randn(layer_sizes[1], layer_sizes[2])
        self.b1 = np.random.randn(layer_sizes[1], 1)
        self.b2 = np.random.randn(layer_sizes[2], 1)

    def activation(self, x):
        sigmoid = 1 / (1 + np.exp(-x))
        return sigmoid

    def forward(self, x):
        A0 = x

        Z1 = self.W1.T @ A0 + self.b1
        A1 = self.activation(Z1)

        Z2 = self.W2.T @ A1 + self.b2
        A2 = self.activation(Z2)

        return A2
