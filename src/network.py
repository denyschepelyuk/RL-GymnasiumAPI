import numpy as np
from typing import List, Any

class FeedForwardNet:
    """
    A simple feed-forward neural network that decodes a flat weight vector into
    weights and biases for each layer and provides an `act` interface.
    """
    def __init__(self, layer_sizes: List[int]):
        """
        Args:
            layer_sizes: list of layer sizes, including input and output dims.
                         e.g. [obs_dim, hidden1, hidden2, action_dim]
        """
        self.layer_sizes = layer_sizes
        # Precompute shapes and total number of weights
        self.shapes = [(layer_sizes[i], layer_sizes[i+1]) for i in range(len(layer_sizes)-1)]
        self.num_weights = sum(in_dim * out_dim + out_dim for in_dim, out_dim in self.shapes)
        # Placeholders for decoded parameters
        self.weights: List[np.ndarray] = []
        self.biases: List[np.ndarray] = []

    def decode(self, genome: np.ndarray) -> None:
        """
        Decode a flat genome vector into the network's weight matrices and biases.

        Args:
            genome: 1D numpy array of length self.num_weights
        """
        assert genome.shape[0] == self.num_weights, (
            f"Genome length {genome.shape[0]} does not match expected {self.num_weights}"
        )
        self.weights = []
        self.biases = []
        idx = 0
        for (in_dim, out_dim) in self.shapes:
            w_size = in_dim * out_dim
            b_size = out_dim
            W = genome[idx: idx + w_size].reshape(in_dim, out_dim)
            idx += w_size
            b = genome[idx: idx + b_size]
            idx += b_size
            self.weights.append(W)
            self.biases.append(b)

    def act(self, obs: Any, discrete: bool = True) -> Any:
        """
        Forward-pass through the network and select an action.

        Args:
            obs: single observation (e.g. numpy array)
            discrete: if True, returns int via argmax; else returns raw network output
        """
        # Ensure genome has been decoded
        assert self.weights and self.biases, "Network parameters not decoded. Call decode() first."

        x = np.array(obs, dtype=np.float32)
        # Forward through hidden layers with tanh activation
        for W, b in zip(self.weights[:-1], self.biases[:-1]):
            x = np.tanh(x @ W + b)
        # Output layer
        logits = x @ self.weights[-1] + self.biases[-1]

        if discrete:
            return int(np.argmax(logits))
        else:
            return logits
