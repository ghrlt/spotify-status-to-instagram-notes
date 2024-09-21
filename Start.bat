@echo off
title Spotify Status to Instagram notes
mode con: cols=125 lines=30
color f
:::
:::  ______                         __      __   ______              ______     __                  __                         
::: /      \                       |  \    |  \ /      \            /      \   |  \                |  \                        
:::|  $$$$$$\  ______    ______   _| $$_    \$$|  $$$$$$\ __    __ |  $$$$$$\ _| $$_     ______   _| $$_    __    __   _______ 
:::| $$___\$$ /      \  /      \ |   $$ \  |  \| $$_  \$$|  \  |  \| $$___\$$|   $$ \   |      \ |   $$ \  |  \  |  \ /       \
::: \$$    \ |  $$$$$$\|  $$$$$$\ \$$$$$$  | $$| $$ \    | $$  | $$ \$$    \  \$$$$$$    \$$$$$$\ \$$$$$$  | $$  | $$|  $$$$$$$
::: _\$$$$$$\| $$  | $$| $$  | $$  | $$ __ | $$| $$$$    | $$  | $$ _\$$$$$$\  | $$ __  /      $$  | $$ __ | $$  | $$ \$$    \ 
:::|  \__| $$| $$__/ $$| $$__/ $$  | $$|  \| $$| $$      | $$__/ $$|  \__| $$  | $$|  \|  $$$$$$$  | $$|  \| $$__/ $$ _\$$$$$$\
::: \$$    $$| $$    $$ \$$    $$   \$$  $$| $$| $$       \$$    $$ \$$    $$   \$$  $$ \$$    $$   \$$  $$ \$$    $$|       $$
:::  \$$$$$$ | $$$$$$$   \$$$$$$     \$$$$  \$$ \$$       _\$$$$$$$  \$$$$$$     \$$$$   \$$$$$$$    \$$$$   \$$$$$$  \$$$$$$$ 
:::          | $$                                        |  \__| $$                                                            
:::          | $$                                         \$$    $$                                                            
:::           \$$                                          \$$$$$$                                                             
:::                                                                                                                         
:::                                                                                                                         
:::                                                                                                                         
:::
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
)
echo Initializing the virtual environment...
echo.
timeout /t 3 /nobreak > NUL
powershell -Command ^
    "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms') | Out-Null;" ^
    "$result = [System.Windows.Forms.MessageBox]::Show('Have the requirements already been installed? Click Yes to skip installation, No to install them.', 'Requirements Check', [System.Windows.Forms.MessageBoxButtons]::YesNo, [System.Windows.Forms.MessageBoxIcon]::Question);" ^
    "if ($result -eq [System.Windows.Forms.DialogResult]::Yes) { exit 6 } else { exit 7 }"

if %errorlevel% equ 6 goto :A
python -m pip install --upgrade pip

set requirements=^
instagrapi ^ 
pillow ^ 
requests ^ 
python-dotenv ^ 
flask

for %%p in (%requirements%) do (
    echo Installing %%p...
    pip install %%p
)
echo All packages installed successfully.
:A
timeout /t 3 /nobreak > NUL

cls
for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
)
echo Scripted by ghrlt                                UI by LytexWZ
echo.
echo This app is in constant development, check latest release at:
echo https://github.com/ghrlt/spotify-status-to-instagram-notes
echo.
python3.10 app.py
echo.
echo.
echo #===============================================================# 
echo #                    Software terminated.                       # 
echo #                                                               # 
echo #   Give me a Star on Github, this would really help me grow!   # 
echo #                 https://github.com/ghrlt                      # 
echo #                                                               #
echo #                                                               #
echo #                         Thank You!                            #
echo #===============================================================# 
echo.
echo.
pause
