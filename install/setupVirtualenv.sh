echo "Setting up virtual environment..."
DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(dirname "$DIR")"
VENV_DIR=$APP_DIR/venv
python3.10 -m venv "$VENV_DIR"
