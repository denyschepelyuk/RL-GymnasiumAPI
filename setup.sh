#!/usr/bin/env bash
set -euo pipefail


# 1. Ensure Python 3.8+
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 not found. Please install Python 3.8 or newer." >&2
  exit 1
fi
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED="3.8"
if [[ "$(printf '%s\n' "$REQUIRED" "$PYVER" | sort -V | head -n1)" != "$REQUIRED" ]]; then
  echo "Error: Python ${REQUIRED}+ required, you have ${PYVER}" >&2
  exit 1
fi

# 2. Create virtual environment
echo "Creating virtualenv in .venv/"
python3 -m venv .venv

# 3. Activate it
# shellcheck source=/dev/null
source .venv/bin/activate

# 4. Upgrade pip, wheel, setuptools
echo "Upgrading pip, wheel, setuptools"
pip install --upgrade pip wheel setuptools

# 5. Install requirements
if [[ -f requirements.txt ]]; then
  echo "Installing requirements.txt"
  pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found, skipping"
fi

# 6. Install package in editable mode (so `src/` is on PYTHONPATH)
if [[ -f setup.py ]]; then
  echo "Installing package in editable mode"
  pip install -e .
else
  echo "Note: no setup.py found; you can still run scripts by adding src/ to PYTHONPATH"
fi

# 7. Create directories for outputs
for dir in logs results; do
  if [[ ! -d $dir ]]; then
    mkdir "$dir"
    echo "Created directory: $dir/"
  fi
done

# 8. (Optional) Copy example config
if [[ -f experiments.yaml.example ]] && [[ ! -f experiments.yaml ]]; then
  cp experiments.yaml.example experiments.yaml
  echo "Copied example config to experiments.yaml—edit as needed."
fi

echo "Setup complete! To start training, try:"
echo ""
echo "  source .venv/bin/activate"
echo "  bash scripts/run_all.sh"
