#!/usr/bin/env bash
set -euo pipefail

# Determine project root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

# Activate the virtual environment
if [[ -f "${PROJECT_ROOT}/.venv/bin/activate" ]]; then
  # shellcheck source=/dev/null
  source "${PROJECT_ROOT}/.venv/bin/activate"
else
  echo "Error: Virtual environment not found. Please run setup.sh first." >&2
  exit 1
fi

# Ensure src/ is on PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

# Create logs directory if missing
mkdir -p "${PROJECT_ROOT}/logs"

# Run the trainer for all experiments defined in experiments.yaml
# Forward any additional arguments (e.g. -e CartPole-v1) to trainer.py
python "${PROJECT_ROOT}/src/trainer.py" "$@"

# Print completion message
echo "All experiments completed. Logs are in ${PROJECT_ROOT}/logs/"
