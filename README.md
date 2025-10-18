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
| Name               | Description                                                       | Type       | Example                   |
|--------------------|-------------------------------------------------------------------|------------|---------------------------|
| `DEBUG`            | Enable debug mode                                                 | bool       | `DEBUG = True`            |
| `LOG_LEVEL`        | Logging level (`DEBUG`/`INFO`/`WARNING`/`ERROR`/`FATAL`)          | str        | `LOG_LEVEL = INFO`        |
| `LOG_COLORFUL`     | Enable colorful logs (requires `rich` to be installed)            | bool       | `LOG_COLORFUL = True`     |
| `TARGET_CONTRACTS` | Currently active contracts for stats (`auto` - get from firebase) | str \| int | `TARGET_CONTRACTS = 100`  |
| `TARGET_CLIENTS`   | Total clients served for stats (`auto` - get from firebase)       | str \| int | `TARGET_CLIENTS = 860`    |
| `TARGET_CARS`      | Total cars in fleet for stats (`auto` - get from firebase)        | str \| int | `TARGET_CARS = 170`       |
| `TAGET_NEW`        | New clients this month for stats (`auto` - get from firebase)     | str \| int | `TARGET_NEW = auto`       |
| `STATS_DURATION`   | Duration to statistic appear in milliseconds                      | int        | `STATS_DURATION = 1000`   |

