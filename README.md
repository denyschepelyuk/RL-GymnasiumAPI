# RL-GymnasiumAPI

---

Reinforcement Learning with using GymnasiumAPI environments 

---

## Usage

---

```
# 1. Clone the repo and enter it
git clone https://github.com/denyschepelyuk/RL-GymnasiumAPI.git
cd RL-GymnasiumAPI


# 2. Run prepared setup script to create a virtual environment and install dependencies
#   and activate newly created virtual environment
./setup.sh
source .venv/bin/activate


# 3. Run all experiments (this will generate CSV logs in ./logs/)
bash scripts/run_all.sh

#    argument -e allows you to filter to specific envs:
bash scripts/run_all.sh -e CartPole-v1 LunarLander-v2


# 4. Analyze results (this will create plots and summaries under ./results/)
bash scripts/analyze_results.sh
#    Or point to custom log/result dirs:
# bash scripts/analyze_results.sh --input_dir ./logs --output_dir ./results

# 5. Deactivate when you’re done
deactivate
```

---

## Project Structure:

---

```plaintext
RL-GymnasiumAPI/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py               # if you want to pip-install your package
├── experiments.yaml       # list of envs + hyperparameter presets
├── src/
│   ├── __init__.py
│   ├── config.py          # parse experiments.yaml or CLI args
│   ├── env_runner.py      # EnvRunner class (reset/step/evaluate)
│   ├── network.py         # FeedForwardNet (decode genome → weights, act())
│   ├── ga.py              # GeneticAlgorithm (init, select, cross, mutate)
│   ├── trainer.py         # train_on_env() orchestrator
│   └── utils.py           # logging, seeding, CSV I/O, plotting helpers
├── scripts/
│   ├── run_all.sh         # loops through envs/seeds, kicks off trainer.py
│   └── analyze_results.py # collate CSVs → plots (mean±std per generation)
├── logs/                  # (auto-created) raw CSVs per env & seed
├── results/               # (auto-created) final plots and summary tables
└── notebooks/
    └── exploratory.ipynb  # for quick experiments or visualizations
```