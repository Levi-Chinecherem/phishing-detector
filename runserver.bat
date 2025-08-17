@echo off

set VENV_DIR=env
set MODEL_FILE=models\random_forest_model.pkl
set URL=http://127.0.0.1:8000
set REPO_URL=git@github.com:Levi-Chinecherem/phishing-detector.git

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

:: Configure Git remote
echo Configuring Git remote...
git remote remove origin 2>NUL
git remote add origin %REPO_URL%
git remote -v

:: Check if model exists, train if not
if not exist %MODEL_FILE% (
    echo Training model...
    python src\train_model.py
)

:: Run test URLs
echo Testing URLs...
python src\test_urls.py

:: Start FastAPI server
echo Starting FastAPI server...
start /B uvicorn main:app --host 127.0.0.1 --port 8000 --reload

:: Wait a moment to ensure server starts
timeout /t 2

:: Open browser
start "" "%URL%"