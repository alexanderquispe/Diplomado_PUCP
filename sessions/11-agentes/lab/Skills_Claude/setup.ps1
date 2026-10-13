Write-Host "Creating Python virtual environment..."
python -m venv .venv

Write-Host "Installing dependencies..."
.\.venv\Scripts\pip install --upgrade pip -q
.\.venv\Scripts\pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete!"
Write-Host "Next steps:"
Write-Host "  1. Open Claude Code from this folder (Skills_Claude/)"
Write-Host "  2. Verify MCP server: type /mcp in Claude Code — 'bcrp' should appear"
Write-Host "  3. Run the dashboard: type /bcrp-dashboard in Claude Code"
