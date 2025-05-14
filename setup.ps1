# Script de configuración para Integral Service SPA

# Configurar PowerShell para usar UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$env:PYTHONIOENCODING = "utf-8"

Write-Host "=== Configuración inicial de Integral Service SPA ===" -ForegroundColor Green

# Cambiar al directorio del proyecto
Set-Location -Path 'e:/repos/MCPs/file/industrial_services_app'

# Configurar la codificación del sistema
Write-Host "`n=== Configurando codificación del sistema ===" -ForegroundColor Green
[System.Environment]::SetEnvironmentVariable('PYTHONIOENCODING', 'utf-8', [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable('PGCLIENTENCODING', 'utf-8', [System.EnvironmentVariableTarget]::User)

# Activar el entorno de Anaconda si está disponible
if (Get-Command "conda" -ErrorAction SilentlyContinue) {
    Write-Host "`nActivando entorno de Anaconda..." -ForegroundColor Yellow
    conda activate integral_service
} else {
    Write-Host "`nAnaconda no encontrado, usando Python del sistema..." -ForegroundColor Yellow
}

# Instalar dependencias
Write-Host "`n=== Instalando dependencias ===" -ForegroundColor Green
python -m pip install -r requirements.txt

# Verificar la codificación de la base de datos
Write-Host "`n=== Verificando codificación de la base de datos ===" -ForegroundColor Green
python database/check_encoding.py

# Verificar y configurar la base de datos
Write-Host "`n=== Configurando base de datos ===" -ForegroundColor Green
python database/check_connection.py

# Si todo está bien, iniciar la aplicación
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Configuración completada exitosamente ===" -ForegroundColor Green
    Write-Host "`nPara iniciar la aplicación, ejecute:" -ForegroundColor Yellow
    Write-Host "streamlit run main.py" -ForegroundColor Cyan
} else {
    Write-Host "`n=== Error en la configuración ===" -ForegroundColor Red
    Write-Host "Por favor, revise los errores anteriores y vuelva a intentarlo" -ForegroundColor Red
}
