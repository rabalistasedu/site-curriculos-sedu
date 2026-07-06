@echo off
cd "C:\Users\ridan\Claude\Projects\Site Curriculos SEDU"
powershell -NoProfile -ExecutionPolicy Bypass -Command "git add . ; git commit -m 'Backup autom?tico - $(Get-Date -Format 'dd/MM/yyyy HH:mm')' ; git push origin master:main"
echo.
echo Enviado com sucesso!
pause
