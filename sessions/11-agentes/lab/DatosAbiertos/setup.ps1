Write-Host "Creating Python virtual environment..."
python -m venv .venv

Write-Host "Installing dependencies..."
.\.venv\Scripts\pip install --upgrade pip -q
.\.venv\Scripts\pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete!"
Write-Host "Next steps:"
Write-Host "  1. Open Cursor with this folder (DatosAbiertos/) as workspace root"
Write-Host "  2. Enable MCP server 'datosabiertos' in Settings -> MCP"
Write-Host "  3. Run: .\.venv\Scripts\python discover_resources.py  (validate catalog)"
Write-Host "  4. In Agent chat: use the datosabiertos-dashboard skill"
