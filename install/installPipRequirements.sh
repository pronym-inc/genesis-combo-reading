echo "Installing pip requirements..."
DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(dirname "$DIR")"
VENV_DIR=$APP_DIR/venv
"$VENV_DIR"/bin/pip3.10 install -r "$APP_DIR"/requirements.txt --upgrade