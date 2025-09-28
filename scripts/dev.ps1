# dev.ps1
# Run FastAPI server in debug mode (auto-reload, debug output)


# Запуск сервера
uvicorn app.main:app `
  --reload `
  --host 0.0.0.0 `
  --port 8000 `
  --log-level warning `
  --no-access-log
