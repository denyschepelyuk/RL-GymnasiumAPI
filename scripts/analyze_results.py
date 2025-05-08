#!/usr/bin/env python3
"""
Aggregate and plot the results of neuroevolution experiments.
Reads CSV logs from a per-environment directory structure and
saves aggregated statistics and plots into mirrored subfolders.
"""

import os
import glob
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(
        description="Aggregate CSV logs and plot mean±std performance curves"
    )
    parser.add_argument(
        '--input_dir', type=str, default='logs',
        help='Directory containing per-env subfolders of CSV logs'
    )
    parser.add_argument(
        '--output_dir', type=str, default='results',
        help='Directory to save per-env plots and summary CSVs'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir

    # Find all CSV files in logs/<env_id>/*.csv
    pattern = os.path.join(input_dir, '*', '*.csv')
    csv_paths = glob.glob(pattern, recursive=True)
    if not csv_paths:
        print(f"No CSV files found in '{input_dir}'.")
        return

    # Read and tag each DataFrame with its env_id (parent folder name)
    records = []
    for path in csv_paths:
        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f"  Skipping '{path}': could not read CSV ({e})")
            continue

        # Extract env_id from the folder name: logs/<env_id>/seedX.csv
        env_id = os.path.basename(os.path.dirname(path))
        df['env_id'] = env_id
        records.append(df)

    if not records:
        print("No valid CSV logs to process.")
        return

    # Concatenate all logs
    data = pd.concat(records, ignore_index=True)

    # Group by env and generation, compute mean & std of best_fitness
    stats = (
        data
        .groupby(['env_id', 'generation'])['best_fitness']
        .agg(['mean', 'std'])
        .reset_index()
    )

    # For each environment, save plot and CSV into results/<env_id>/
    for env_id, group in stats.groupby('env_id'):
        env_out = os.path.join(output_dir, env_id)
        os.makedirs(env_out, exist_ok=True)

        # Plot mean ± std
        fig, ax = plt.subplots()
        ax.plot(group['generation'], group['mean'], label='Mean')
        ax.fill_between(
            group['generation'],
            group['mean'] - group['std'],
            group['mean'] + group['std'],
            alpha=0.3,
            label='Std Dev'
        )
        ax.set_title(f"Neuroevolution Performance on {env_id}")
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.legend()
        ax.grid(True)

        # Save plot
        plot_path = os.path.join(env_out, f"{env_id}.png")
        fig.savefig(plot_path)
        plt.close(fig)

        # Save stats CSV
        summary_path = os.path.join(env_out, f"{env_id}_stats.csv")
        group.to_csv(summary_path, index=False)

        print(f"Saved results for {env_id}:")
        print(f"  Plot → {plot_path}")
        print(f"  Data → {summary_path}")

    print("Analysis complete.")

if __name__ == '__main__':
    main()
