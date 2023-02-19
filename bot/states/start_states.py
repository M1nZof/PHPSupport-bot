from enum import Enum, auto


class States(Enum):
    ROLE = auto()
    FREELANCE_START = auto()
    FREELANCE_ORDERS = auto()
    CUSTOMER_START = auto()
    CUSTOMER_SUBSCRIBE = auto()
    CUSTOMER_ORDERS = auto()
    FREELANCE_CHOICE_ORDERS = auto()
