@echo off
REM Активировать виртуальное окружение
call .venv\Scripts\activate

REM Запустить программу на Python
python main.py

REM Деактивировать виртуальное окружение
deactivate
