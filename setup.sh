#!/usr/bin/env bash
set -euo pipefail

# 0. Go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Ensure Python 3.8+ is installed
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 not found. Install Python 3.8+." >&2
  exit 1
fi
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$(printf '%s\n' "3.8" "$PYVER" | sort -V | head -n1)" != "3.8" ]]; then
  echo "Error: Python 3.8+ required (you have $PYVER)." >&2
  exit 1
fi

# 2. Create (or recreate) the virtualenv
echo "Creating virtualenv in .venv/…"
rm -rf .venv
python3 -m venv .venv

# 3. Activate it
# shellcheck source=/dev/null
source .venv/bin/activate

# 4. Define venv-python3 explicitly
VENV_PYTHON3="$(pwd)/.venv/bin/python3"
echo "Using venv python3: $VENV_PYTHON3"

# 5. Upgrade packaging tools via the venv’s python3
echo "Upgrading pip, wheel, setuptools…"
"$VENV_PYTHON3" -m pip install --upgrade pip wheel setuptools

# 6. Install project dependencies from requirements.txt
if [[ -f requirements.txt ]]; then
  echo "Installing dependencies from requirements.txt…"
  "$VENV_PYTHON3" -m pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found; skipping."
fi

# 7. Ensure logs/ and results/ directories exist
for d in logs results; do
  if [[ ! -d "$d" ]]; then
    mkdir -p "$d"
    echo "Created directory $d/"
  fi
done

# 8. Make scripts executable
if [[ -d scripts ]]; then
  chmod +x scripts/*.sh scripts/*.py || true
fi

echo -e "\n✅ Setup complete!"
echo "Next:"
echo "  source .venv/bin/activate"
echo "  bash scripts/run_all.sh"
