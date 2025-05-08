#!/usr/bin/env bash
set -euo pipefail

# 0) Jump to the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1) Ensure Python 3.8+ is installed
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 not found. Please install Python 3.8 or newer." >&2
  exit 1
fi
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$(printf '%s\n' "3.8" "$PYVER" | sort -V | head -n1)" != "3.8" ]]; then
  echo "Error: Python 3.8+ required (you have $PYVER)." >&2
  exit 1
fi

# 2) Create the virtual environment if needed
if [[ ! -d .venv ]]; then
  echo "Creating virtualenv in .venv/"
  python3 -m venv .venv
else
  echo "Virtualenv .venv already exists; skipping creation."
fi

# 3) Activate it
# shellcheck disable=SC1091
source .venv/bin/activate

# 4) Use the venv's python3 explicitly
VENV_PYTHON3="$(pwd)/.venv/bin/python3"
echo "Using venv python: $VENV_PYTHON3"

# 5) Upgrade pip, wheel, setuptools
echo "Upgrading pip, wheel, setuptools..."
"$VENV_PYTHON3" -m pip install --upgrade pip wheel setuptools

# 6) Install dependencies from requirements.txt
REQ_FILE="requirements.txt"
if [[ -f "$REQ_FILE" ]]; then
  echo "Installing dependencies from $REQ_FILE..."
  "$VENV_PYTHON3" -m pip install -r "$REQ_FILE"
else
  echo "Warning: $REQ_FILE not found; skipping dependency installation."
fi

# 7) Ensure logs/ and results/ directories exist
for dir in logs results; do
  if [[ ! -d "$dir" ]]; then
    mkdir -p "$dir"
    echo "Created directory: $dir/"
  fi
done

# 8) Make scripts executable
if [[ -d scripts ]]; then
  chmod +x scripts/*.sh scripts/*.py 2>/dev/null || true
fi

echo -e "\n✅ Setup complete!"
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  bash scripts/run_all.sh"
echo "  bash scripts/analyze_results.sh"
