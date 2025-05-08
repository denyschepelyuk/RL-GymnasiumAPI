import gymnasium as gym
from typing import Any, Optional


class EnvRunner:
    """
    A generic runner for Gymnasium environments that handles seeding,
    observation/action dimensions, and evaluation of a policy network.
    """
    def __init__(self, env_id: str, seed: Optional[int] = None):
        """
        Initialize the environment.

        Args:
            env_id:      The Gymnasium environment ID (e.g. 'CartPole-v1').
            seed:        Optional random seed for reproducibility.
        """
        self.env_id = env_id
        self.env = gym.make(env_id)

        # Seed the environment (action & observation spaces) if provided
        self.seed = seed
        if seed is not None:
            try:
                # Newer Gym API: seed both spaces
                self.env.reset(seed=seed)
                self.env.action_space.seed(seed)
                self.env.observation_space.seed(seed)
            except TypeError:
                # Fallback for older versions
                self.env.seed(seed)

        # Determine observation dimension
        obs_space = self.env.observation_space
        if hasattr(obs_space, 'shape') and obs_space.shape:
            self.obs_dim = obs_space.shape[0]
        else:
            self.obs_dim = None  # e.g. for Dict or non-array spaces

        # Determine action dimension and type
        act_space = self.env.action_space
        if hasattr(act_space, 'n'):
            self.action_dim = act_space.n
            self.is_discrete = True
        elif hasattr(act_space, 'shape') and act_space.shape:
            self.action_dim = act_space.shape[0]
            self.is_discrete = False
        else:
            self.action_dim = None
            self.is_discrete = False

    def evaluate(self, network: Any, episodes: int = 5, render: bool = False) -> float:
        """
        Evaluate a policy network over a number of episodes.

        Args:
            network:  An object with method act(obs, discrete) -> action.
            episodes: Number of episodes to average over.
            render:   Whether to render the environment during evaluation.

        Returns:
            The average total reward across episodes.
        """
        total_reward = 0.0

        for ep in range(episodes):
            # Optionally reseed per-episode for reproducibility
            reset_seed = None
            if self.seed is not None:
                reset_seed = self.seed + ep
            obs, _ = self.env.reset(seed=reset_seed)
            done = False
            ep_reward = 0.0

            while not done:
                action = network.act(obs, discrete=self.is_discrete)
                obs, reward, terminated, truncated, info = self.env.step(action)
                if render:
                    self.env.render()
                ep_reward += reward
                done = terminated or truncated

            total_reward += ep_reward

        avg_reward = total_reward / episodes
        return avg_reward

    def close(self) -> None:
        """
        Close the environment and any rendering windows.
        """
        self.env.close()
