from logging import getLogger
from dateutil.parser import parse

logger = getLogger('desicars')


def _format_phone(data: str | None) -> int | None:
    if data is None:
        return
    data = data.lstrip('+').replace('(', '').replace(')', '').replace('-', '')
    if data.isdigit():
        return int(data)
    logger.warning('found unparseable phone: %s', data)

def _format_plate(data: str) -> str | None:
    if data in ('-', '', ' '):
        return
    return data

def _format_status(data: str) -> str:
    data = data.lower()
    if data in ('free', 'свободна'):
        return 'free'
    if data in ('rent', 'занята', 'аренда'):
        return 'rent'
    if data in ('archive', 'архив'):
        return 'archive'
    logger.warning('found unparseable status: %s', data)
    return 'none'

def map_car(data: dict) -> dict:
    return {
        'changeoil': {
            'start': data.get('OilChange_Start'),
            'end': data.get('OilChange_End')
        },
        'nickname': data['nickname'],
        'odometer': data['odometer'],
        'vehicle': {
            'color': data.get('color'),
            'make': data.get('make') or data.get('vehicle'),
            'model': data.get('model'),
            'year': data.get('year') or int(data.get('year_string', '0')),
            'name': f'{data["make"] or data["vehicle"]} {data["model"]}' if 'model' in data and 'make' in data or 'vehicle' in data else None
        },
        'tolltag': data.get('toltag', '').lstrip('NTTA'),
        'vin': data.get('vin'),
        'plate': _format_plate(data.get('plate', '')),
        'price': data.get('def_price'),
        'imei': int(data.get('device_imei', '0')),
        'engine': float(data.get('engine', '0L').rstrip('L')),
        'fuel': round(float(data.get('fuel', 0.0)), 2),
        'relay_id': data.get('idRelay'),
        'relay_block': data.get('relayBlocked', False),
        'gps_phone': _format_phone(data.get('gpsTrackerPhone')),
        'photos': data.get('photo_album', []),
        'status': _format_status(data['status']),
        'timestamps': {
            'registration_end': data.get('TO_end'),
            'last_seen': parse(data.get('last_seen', '2000-01-01 00:00:00'))
        }
    }