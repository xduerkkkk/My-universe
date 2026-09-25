@echo off
REM Obsidian Vault 自动备份脚本
REM 用法: 双击运行，或放到任务计划程序每天自动执行

set VAULT_PATH=C:\Users\kkkkkk\OneDrive\OneSyncFiles\universe
set BACKUP_ROOT=D:\ObsidianBackup
set DATE_STAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATE_STAMP=%DATE_STAMP: =0%

set BACKUP_PATH=%BACKUP_ROOT%\vault_backup_%DATE_STAMP%

echo [%date% %time%] 开始备份 Obsidian Vault...
echo 源目录: %VAULT_PATH%
echo 目标目录: %BACKUP_PATH%

REM 创建备份目录
if not exist "%BACKUP_ROOT%" mkdir "%BACKUP_ROOT%"

REM 使用 robocopy 进行增量备份（速度快、占用少）
robocopy "%VAULT_PATH%" "%BACKUP_PATH%" /MIR /XD .git node_modules .obsidian\workspace* /R:3 /W:5 /LOG:"%BACKUP_ROOT%\backup_log.txt"

echo [%date% %time%] 备份完成！
echo.
echo 保留最近7天备份，删除旧备份...

REM 删除7天前的备份（可选）
forfiles /p "%BACKUP_ROOT%" /m vault_backup_* /d -7 /c "cmd /c if @isdir==TRUE rd /s /q @path" 2>nul

echo 完成！按任意键退出...
pause >nul
