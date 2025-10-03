# desicars.us
**[Software Requirements Specification](./SRS.docx)**

Website for DesiCars (car rental company)

## Run
### .env
```bash
cp .env.example .env
```

### Development
```bash
pip install -r requirements-dev.txt
./scripts/dev.ps1
```
### Production
```bash
pip install -r requirements.txt
./scripts/prod.sh
```

## Configuration
All configuration provides in `.env` file.
| Name              | Description                                              | Type   | Example               |
|-------------------|----------------------------------------------------------|--------|-----------------------|
| `DEBUG`           | Enable debug mode                                        | bool   | `DEBUG = True`        |
| `LOG_LEVEL`       | Logging level (`DEBUG`/`INFO`/`WARNING`/`ERROR`/`FATAL`) | str    | `LOG_LEVEL = INFO`    |
| `LOG_COLORFUL`    | Enable colorful logs (requires `rich` to be installed)   | bool   | `LOG_COLORFUL = True` |
