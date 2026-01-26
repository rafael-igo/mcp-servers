# Script para reiniciar todos os MCPs no servidor
# Execute: .\restart-mcps.ps1

Write-Host "🔄 Parando containers existentes..." -ForegroundColor Yellow
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose down"

Write-Host ""
Write-Host "🚀 Subindo todos os 10 MCPs..." -ForegroundColor Green
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose up -d"

Write-Host ""
Write-Host "✅ Verificando status..." -ForegroundColor Cyan
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose ps"

Write-Host ""
Write-Host "🎉 Pronto! Todos os MCPs devem estar rodando." -ForegroundColor Green
Write-Host ""
Write-Host "Para testar:" -ForegroundColor Yellow
Write-Host "  1. Abra VSCode/Cursor"
Write-Host "  2. Reload Window (Ctrl+Shift+P → Reload Window)"
Write-Host "  3. Teste: docker-admin.health_check()"
