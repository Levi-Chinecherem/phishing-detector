#!/bin/bash

VENV_DIR="env"
MODEL_FILE="models/random_forest_model.pkl"
URL="http://127.0.0.1:8000"
REPO_URL="git@github.com:Levi-Chinecherem/phishing-detector.git"

# Set PYTHONPATH to project root
export PYTHONPATH=$(pwd):$PYTHONPATH

# Check if virtual environment exists, create if not
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Configure Git remote
echo "Configuring Git remote..."
git remote remove origin 2>/dev/null || true
git remote add origin $REPO_URL
git remote -v

# Check if model exists, train if not
if [ ! -f "$MODEL_FILE" ]; then
    echo "Training model..."
    python src/train_model.py
fi

# Run test URLs
echo "Testing URLs..."
python src/test_urls.py

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn main:app --host 127.0.0.1 --port 8000 --reload &

# Wait a moment to ensure server starts
sleep 2

# Open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "$URL"
else
    echo "Please open $URL in your web browser."
fi