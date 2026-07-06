cd "C:\Users\ridan\Claude\Projects\Site Curriculos SEDU"
git add .
git commit -m "Backup automático - $(Get-Date -Format 'dd/MM/yyyy HH:mm')"
git push origin master:main
Write-Host ""
Write-Host "Enviado com sucesso!" -ForegroundColor Green
Read-Host "Pressione ENTER para sair"
