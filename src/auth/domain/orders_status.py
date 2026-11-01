from enum import StrEnum

class OrderStatus(StrEnum):
    NEW = "new"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
