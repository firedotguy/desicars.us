from enum import Enum


class CarType(Enum):
    GASOLINE = "gasoline"
    HYBRID = "hybrid"
    MINIVAN = "minivan"


class CarColor(Enum):
    BLACK = "black"
    WHITE = "white"
    SILVER = "silver"
    RED = "red"
    GREEN = "green"
    GRAY = "gray"
    BLUE = "blue"
    GOLD = "gold"


class CarStatus(Enum):
    FREE = "free"
    RENT = "rent"
    CRASH = "crash"
    ARCHIVE = "archive"


class CarMake(Enum):
    TOYOTA = 'Toyota'
    VOLKSWAGEN = 'Volkswagen'
    NISSAN = 'Nissan'
    KIA = 'KIA'
    FORD = 'Ford'
    HONDA = 'Honda'
    ACURA = 'Acura'
    LEXUS = 'Lexus'
    DODGE = 'Dodge'
    HYUNDAI = 'Hyundai'
    MAZDA = 'Mazda'
    CHEVROLET = 'Chevrolet'


class CarSorting(Enum):
    MODEL = 'model'
    PRICE_ASC = 'price-asc'
    PRICE_DESC = 'price-desc'
    YEAR = 'year'