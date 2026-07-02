@echo off
echo ==========================================
echo    Smart Campus App - Python ^& SQLite
echo ==========================================
echo.
echo [1/3] Installing/updating required python libraries...
pip install -r backend\requirements.txt

echo.
echo [2/3] Initializing SQLite database...
python backend\init_db.py

echo.
echo [3/3] Starting backend Flask server...
start "Smart Campus Backend (Flask)" cmd /k "cd backend && python app.py"

echo.
echo Opening the frontend in your default browser...
start index.html


echo.
echo Done! App is now running.
echo You can use Student Portal or Admin Portal.
echo Admin credentials: admin@campus.com / admin123
echo.
pause
