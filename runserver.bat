@echo off

set VENV_DIR=env
set MODEL_FILE=models\random_forest_model.pkl
set URL=http://127.0.0.1:8000

:: Check if virtual environment exists, create if not
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Check if model exists, train if not
if not exist %MODEL_FILE% (
    echo Training model...
    python src\train_model.py
)

:: Start FastAPI server
echo Starting FastAPI server...
start /B uvicorn main:app --host 127.0.0.1 --port 8000 --reload

:: Wait a moment to ensure server starts
timeout /t 2

:: Open browser
start "" "%URL%"