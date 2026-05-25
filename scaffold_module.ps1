# Script to scaffold a new Odoo 19 module
param(
    [Parameter(Mandatory=$true)]
    [string]$ModuleName
)

$PYTHON_PATH = "c:\Users\Usuario\Desktop\Odoo Antigravity\venv\Scripts\python.exe"
$ODOO_BIN = "c:\Users\Usuario\Desktop\Odoo Antigravity\odoo-bin"
$ADDONS_DIR = "c:\Users\Usuario\Desktop\OC ODOO\custom_addons"

Write-Host "Scaffolding new Odoo module '$ModuleName' into $ADDONS_DIR..." -ForegroundColor Cyan

# Run the scaffold command
& $PYTHON_PATH $ODOO_BIN scaffold $ModuleName $ADDONS_DIR

if ($LASTEXITCODE -eq 0) {
    Write-Host "Success! Your new module skeleton has been generated under custom_addons/$ModuleName" -ForegroundColor Green
    Write-Host "You can now edit its __manifest__.py, models, views, etc." -ForegroundColor Yellow
} else {
    Write-Error "Failed to scaffold the module."
}
