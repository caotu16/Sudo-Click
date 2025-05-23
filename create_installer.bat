@echo off
echo ====================================================
echo           TAO FILE EXE CHO SUDOCLICK
echo ====================================================
echo.
echo Dang kiem tra Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo KHONG TIM THAY PYTHON!
    echo.
    echo Vui long cai dat Python tu: https://www.python.org/downloads/
    echo Chon "Add Python to PATH" khi cai dat!
    echo.
    pause
    exit /b 1
)

echo Python da duoc cai dat!
echo.
echo Dang cai dat PyInstaller va cac thu vien...
pip install pyinstaller pyautogui keyboard

echo.
echo Dang tao file exe cho SUDO Click Global...
echo.

pyinstaller --onefile --windowed --name="SUDO Click" --add-data "sudo_click_global.py;." sudo_click_global.py

if errorlevel 1 (
    echo.
    echo LOI: Khong the tao file exe!
    pause
    exit /b 1
)

echo.
echo ====================================================
echo           TAO FILE EXE THANH CONG!
echo ====================================================
echo.
echo File SuClick.exe da duoc tao trong thu muc dist\
echo.
echo Thong tin phan mem:
echo - Ten: SuClick
echo - Tac gia: Sudo  
echo - Phien ban: 1.0.0
echo - Kich thuoc: khoang 25-35MB
echo.
echo Ban co the:
echo 1. Copy file SuClick.exe sang may khac de chay
echo 2. Khong can cai Python tren may dich
echo 3. Chi can double-click de chay ung dung
echo 4. Chia se de ban be su dung
echo.
pause

if exist "dist\SuClick.exe" (
    echo Mo thu muc chua file exe...
    explorer dist
)