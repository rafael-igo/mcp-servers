@echo off
REM Script para reiniciar todos os MCPs no servidor
echo.
echo ====================================
echo  Reiniciando MCPs no Servidor
echo ====================================
echo.

echo [1/3] Parando containers existentes...
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose down"

echo.
echo [2/3] Subindo todos os 10 MCPs...
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose up -d"

echo.
echo [3/3] Verificando status...
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose ps"

echo.
echo ====================================
echo  Pronto! MCPs rodando no servidor
echo ====================================
echo.
echo Para testar:
echo   1. Abra VSCode/Cursor
echo   2. Reload Window (Ctrl+Shift+P)
echo   3. Teste: docker-admin.health_check()
echo.
pause
