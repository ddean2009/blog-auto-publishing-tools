chcp 65001
@echo off

IF EXIST venv (
    echo venv 目录或文件已存在
    :: Deactivate the virtual environment
    call .\venv\Scripts\deactivate.bat

    :: Activate the virtual environment
    call .\venv\Scripts\activate.bat
    set PATH=%%PATH%%;%%~dp0venv\Lib\site-packages\torch\lib
) ELSE (
    echo venv 目录或文件不存在
)

set "config_dir=config"
set "source_file=%config_dir%\common.default.yaml"
set "target_file=%config_dir%\common.yaml"

if not exist "%target_file%" (
    copy "%source_file%" "%target_file%"
) else (
    echo %target_file% already exists.
)

REM Check if the batch was started via double-click
IF /i "%%comspec%% /c %%~0 " equ "%%cmdcmdline:"=%%" (
    REM echo This script was started by double clicking.
    cmd /k python.exe publish_all.py %*
) ELSE (
    REM echo This script was started from a command prompt.
    python.exe publish_all.py %*
)

