from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    WASHER = "WASHER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"