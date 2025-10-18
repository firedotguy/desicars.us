# dev.ps1
# Run FastAPI server in debug mode (auto-reload, debug output)

uvicorn app.main:app `
  --reload `
  --host 127.0.0.1 `
  --port 1488 `
  --log-level warning `
  --no-access-log
