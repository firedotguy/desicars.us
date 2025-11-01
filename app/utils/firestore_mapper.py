from app.utils.logger import get_logger
from app.enums import CarColor, CarType, CarStatus, CarMake
from app.schemas.car import Car, Vehicle
from app.schemas.contract import ContractSchema

logger = get_logger("firestore_mapper")


def _format_phone(data: str | None) -> int | None:
    if data is None:
        return
    data = data.lstrip("+").replace("(", "").replace(")", "").replace("-", "")
    if data.isdigit():
        return int(data)
    logger.warning("found unparseable phone: %s", data)


def _format_plate(data: str | None) -> str | None:
    if not data or data.strip() in ("-", "", " "):
        return None
    return data.strip()


def _format_status(data: str | None) -> CarStatus:
    if not data:
        return CarStatus.FREE
    data = data.lower()
    if data in ("free", "свободна"):
        return CarStatus.FREE
    if data in ("rent", "занята", "аренда"):
        return CarStatus.RENT
    if data in ("archive", "архив"):
        return CarStatus.ARCHIVE
    if data in ("crash", "сломана", "разбита"):
        return CarStatus.CRASH
    logger.warning("found unparseable car status: %s", data)
    return CarStatus.FREE


def _format_type(data: str | None) -> CarType | None:
    if not data:
        return
    try:
        return CarType(data.strip().lower())
    except ValueError:
        logger.warning("found unparseable car type: %s", data)
        return


def _format_color(data: str | None) -> CarColor | None:
    if not data:
        return
    data = data.strip().lower()
    if data in ("grey", "gray"):
        return CarColor.GRAY
    if data in ("gold", "golden"):
        return CarColor.GOLD
    try:
        return CarColor(data)
    except ValueError:
        logger.warning("found unparseable car color: %s", data)
        return

def _format_make(data: str | None) -> CarMake | None:
    if not data:
        return
    if data.lower() == "kia":
        return CarMake.KIA

    try:
        return CarMake(data.title())
    except ValueError:
        logger.warning("found unparseable car make: %s", data)


def _safe_title(value: str | None) -> str | None:
    if not value or not str(value).strip():
        return None
    return str(value).title()


def map_car(data: dict) -> Car:
    """Map firestore car document -> pydantic Car"""
    return Car(
        # changeoil={
        #     "start": data.get("OilChange_Start"),
        #     "end": data.get("OilChange_End"),
        # },
        nickname=data.get("nickname", "").strip(),
        # odometer=data.get("odometer"),
        vehicle=Vehicle(
            color=_format_color(data.get("color")),
            make=_format_make(data.get("make") or data.get("vehicle")),
            model=_safe_title(data.get("model")),
            year=(data.get("year") or int(data.get("year_string", "0"))) or None,
            name=(
                f"{_safe_title(data.get('make') or data.get('vehicle'))} {_safe_title(data.get('model'))}".strip()
                if data.get("model") and (data.get("make") or data.get("vehicle"))
                else None
            ),
            type=_format_type(data.get("type")),
        ),
        # tolltag=(data.get("toltag") or "").lstrip("NTTA"),
        # vin=data.get("vin"),
        plate=_format_plate(data.get("plate")),
        # imei=int(data.get("device_imei", "0")) if data.get("device_imei") else None,
        engine=(data.get("engine") or None),
        # fuel=round(float(data.get("fuel", 0.0)), 2),
        # renter=data.get("current_renter"),
        price=data.get("def_price"),
        status=_format_status(data.get("status")),
        # relay_id=data.get("idRelay"),
        # relay_block=data.get("relayBlocked", False),
        # gps_phone=_format_phone(data.get("gpsTrackerPhone")),
        web_photos=[p for p in data.get("photo_website", []) if p],
        photos=[p for p in data.get("photo_album", []) if p],
        # timestamps={
        #     "registration_end": data.get("TO_end"),
        #     "last_seen": data.get("last_seen"),
        # },
    )


def map_contract(data: dict) -> ContractSchema:
    """Map Firestore contract document → Pydantic ContractSchema"""
    return ContractSchema(
        active=data.get("Active", False),
        start_odometer=data.get("Begin_odom"),
        payday_odometer=data.get("Payday_odom") or data.get("Begin_odom"),
        state=(data.get("state") or "TX").upper(),
        name=data.get("ContractName", "").strip(),
        nickname=data.get("nickname", "").strip(),
        # document_photos=data.get("DocumentPhoto", []),
        car_photos=data.get("car_photo", []) or [],
        car_close_photos=data.get("photo_after_close") or [],
        price=round(float(data.get("daily_price", 0.0)), 2),
        start_price=data.get("startPrice"),
        deposit=data.get("zalog") or data.get("deposit"),
        # discount=data.get("discount_month", 0),
        # promo_code=data.get("promoCode"),
        mil_limit=data.get("limit"),
        # saldo=data.get("last_saldo", 0),
        # renter={
        #     "name": data.get("renter"),
        #     "phones": [_format_phone(phone) for phone in data.get("renternumber", [])],
        #     "sms_block": data.get("sms_blocked", False),
        #     "address": data.get("address"),
        #     "email": data.get("email"),
        # },
        # insurance={
        #     "company": data.get("insurance"),
        #     "number": data.get("insurance_number"),
        #     "expires_at": data.get("Insurance_end"),
        # },
        # license={
        #     "number": data.get("license"),
        #     "expires_at": data.get("licenseDate"),
        # },
        timestamps={
            "insurance_end": data.get("Insurance_end"),
            # "license_end": data.get("licenseData"),
            "created_at": data.get("begin_time"),
            "ended_at": data.get("end_time"),
            "payday": data["pay_day"].day if data.get("pay_day") else None,
        },
    )
