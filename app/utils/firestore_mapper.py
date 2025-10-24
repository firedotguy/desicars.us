from dateutil.parser import parse

from app.utils.logger import get_logger

logger = get_logger()


def _format_phone(data: str | None) -> int | None:
    if data is None:
        return
    data = data.lstrip("+").replace("(", "").replace(")", "").replace("-", "")
    if data.isdigit():
        return int(data)
    logger.warning("found unparseable phone: %s", data)


def _format_plate(data: str) -> str | None:
    if data in ("-", "", " "):
        return
    return data


def _format_status(data: str) -> str:
    data = data.lower()
    if data in ("free", "свободна"):
        return "free"
    if data in ("rent", "занята", "аренда"):
        return "rent"
    if data in ("archive", "архив"):
        return "archive"
    logger.warning("found unparseable status: %s", data)
    return "none"


def map_car(data: dict) -> dict:
    return {
        "changeoil": {
            "start": data.get("OilChange_Start"),
            "end": data.get("OilChange_End"),
        },
        "nickname": data["nickname"],
        "odometer": data["odometer"],
        "vehicle": {
            "color": data.get("color"),
            "make": data.get("make") or data.get("vehicle"),
            "model": data.get("model"),
            "year": data.get("year") or int(data.get("year_string", "0")),
            "name": (
                f'{data["make"] or data["vehicle"]} {data["model"]}'
                if "model" in data and "make" in data or "vehicle" in data
                else None
            ),
            "type": data.get("type"),
        },
        "tolltag": data.get("toltag", "").lstrip("NTTA"),
        "vin": data.get("vin"),
        "plate": _format_plate(data.get("plate", "")),
        "imei": int(data.get("device_imei", "0")),
        "engine": float(data.get("engine", "0L").rstrip("L")),
        "fuel": round(float(data.get("fuel", 0.0)), 2),
        "renter": data.get("curren_renter"),
        "price": data.get("def_price"),
        "status": _format_status(data["status"]),
        "relay_id": data.get("idRelay"),
        "relay_block": data.get("relayBlocked", False),
        "gps_phone": _format_phone(data.get("gpsTrackerPhone")),
        "web_photos": data.get("photo_website", []),
        "photos": data.get("photo_album", []),
        "timestamps": {
            "registration_end": data.get("TO_end"),
            "last_seen": parse(data.get("last_seen", "2000-01-01 00:00:00")),
        },
    }


def map_contract(data: dict) -> dict:
    return {
        "active": data.get("Active", False),
        "start_odometer": data.get("Begin_odom"),
        "payday_odometer": data.get("Payday_odom") or data.get("Begin_odom"),
        "state": data.get("state", "TX").upper(),
        "name": data["ContractName"],
        "nickname": data["nickname"],
        "document_photos": data.get("DocumentPhoto", []),
        "car_photos": data.get("car_photo", []),
        "car_close_photos": data.get("photo_after_close"),
        "price": round(data.get("daily_price", 0.0), 2),
        "start_price": data.get("startPrice"),
        "deposit": data.get("zalog") or data.get("deposit"),
        "discount": data.get("discount_month", 0),
        "promo_code": data.get("promoCode"),
        "mil_limit": data.get("limit"),
        "saldo": data.get("last_saldo", 0),
        "renter": {
            "name": data.get("renter"),
            "phones": [_format_phone(phone) for phone in data["renternumber"]],
            "sms_block": data.get("sms_blocked", False),
            "address": data.get("address"),
            "email": data.get("email"),
        },
        "insurance": {
            "company": data.get("insurance"),
            "number": data.get("insurance_number"),
            "expires_at": data.get("Insurance_end"),
        },
        "license": {
            "number": data.get("license"),
            "expires_at": data.get("licenseDate"),
        },
        "timestamps": {
            "insurance_end": data.get("Insurance_end"),
            "license_end": data.get("licenseData"),
            "created_at": data.get("begin_time"),
            "ended_at": data.get("end_time"),
            "payday": data["pay_day"].day,
        },
    }
