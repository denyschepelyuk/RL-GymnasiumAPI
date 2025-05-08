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

# Create results directory if missing
mkdir -p "${PROJECT_ROOT}/results"

# Run the analysis script to aggregate and plot results
# Accepts optional args: --input_dir <dir> --output_dir <dir>
python "${PROJECT_ROOT}/scripts/analyze_results.py" --input_dir "${PROJECT_ROOT}/logs" --output_dir "${PROJECT_ROOT}/results" "$@"

# Completion message
echo "Analysis complete. Plots and summary files are in ${PROJECT_ROOT}/results/"
