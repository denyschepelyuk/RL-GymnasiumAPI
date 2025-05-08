#!/usr/bin/env bash
set -euo pipefail

# Determine project root (one level up from this script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

# Activate the virtual environment
VENV_ACTIVATE="${PROJECT_ROOT}/.venv/bin/activate"
if [[ -f "${VENV_ACTIVATE}" ]]; then
  # shellcheck source=/dev/null
  source "${VENV_ACTIVATE}"
else
  echo "Error: Virtual environment not found at ${PROJECT_ROOT}/.venv" >&2
  exit 1
fi

# Use the venv's Python executable for analysis
PYTHON_EXEC="${PROJECT_ROOT}/.venv/bin/python"
if [[ ! -x "${PYTHON_EXEC}" ]]; then
  echo "Error: Python executable not found at ${PYTHON_EXEC}" >&2
  exit 1
fi

# Ensure src/ is on PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

# Verify analysis script exists
ANALYSIS_SCRIPT="${PROJECT_ROOT}/scripts/analyze_results.py"
if [[ ! -f "${ANALYSIS_SCRIPT}" ]]; then
  echo "Error: analyze_results.py not found in scripts directory." >&2
  exit 1
fi

# Create results directory if missing
mkdir -p "${PROJECT_ROOT}/results"

# Run the analysis script, forwarding any arguments
"${PYTHON_EXEC}" "${ANALYSIS_SCRIPT}" \
  --input_dir "${PROJECT_ROOT}/logs" \
  --output_dir "${PROJECT_ROOT}/results" "$@"

# Completion message
echo "Analysis complete. Plots and summaries are in ${PROJECT_ROOT}/results/"
