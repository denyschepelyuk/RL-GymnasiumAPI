import yaml
import argparse
import os

def deep_merge(default: dict, override: dict) -> dict:
    """
    Recursively merge two dictionaries. Values in override take precedence.
    """
    merged = {}  # new dict
    for key in set(default) | set(override):
        if key in default and key in override:
            if isinstance(default[key], dict) and isinstance(override[key], dict):
                merged[key] = deep_merge(default[key], override[key])
            else:
                merged[key] = override[key]
        elif key in override:
            merged[key] = override[key]
        else:
            merged[key] = default[key]
    return merged


def load_experiments(config_path: str) -> list:
    """
    Load experiments from a YAML config, merging defaults with per-experiment settings.

    Returns:
        A list of dicts, each containing the merged settings for an experiment,
        with the key 'env_id' naming the environment.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    default_cfg = config.get('default', {}) or {}
    experiments = config.get('experiments', []) or []
    merged_list = []

    for exp in experiments:
        if 'env' not in exp:
            raise KeyError("Each experiment entry must have an 'env' key specifying the environment ID.")
        merged = deep_merge(default_cfg, exp)
        # rename 'env' to 'env_id'
        merged['env_id'] = merged.pop('env')
        merged_list.append(merged)

    return merged_list


def parse_args():
    parser = argparse.ArgumentParser(
        description="Load and display neuroevolution experiments from a YAML config"
    )
    parser.add_argument(
        '-c', '--config', type=str, default='experiments.yaml',
        help='Path to the experiments YAML configuration file'
    )
    parser.add_argument(
        '-e', '--envs', nargs='*',
        help='List of environment IDs to filter; if omitted, all experiments are returned'
    )
    return parser.parse_args()


def get_experiments() -> list:
    """
    Parse CLI arguments, load experiments, and optionally filter by env IDs.
    """
    args = parse_args()
    exps = load_experiments(args.config)
    if args.envs:
        exps = [exp for exp in exps if exp['env_id'] in args.envs]
    return exps


if __name__ == '__main__':
    # When run as a script, print out each experiment's settings
    experiments = get_experiments()
    for exp in experiments:
        print("Experiment for environment:", exp['env_id'])
        for k, v in exp.items():
            if k != 'env_id':
                print(f"  {k}: {v}")
        print()  # blank line
