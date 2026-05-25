# Script to run Odoo 19 with local configurations
$PYTHON_PATH = "c:\Users\Usuario\Desktop\Odoo Antigravity\venv\Scripts\python.exe"
$ODOO_BIN = "c:\Users\Usuario\Desktop\Odoo Antigravity\odoo-bin"
$CONFIG_FILE = "c:\Users\Usuario\Desktop\OC ODOO\odoo.conf"

# Ensure wkhtmltopdf bin folder is in the PATH for this execution
$env:PATH = "C:\Program Files\wkhtmltopdf\bin;" + $env:PATH

Write-Host "Starting Odoo 19 with config $CONFIG_FILE..." -ForegroundColor Cyan

# Run Odoo with the config file and any additional arguments passed to this script
& $PYTHON_PATH $ODOO_BIN -c $CONFIG_FILE @args

