from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    WASHER = "WASHER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class VehicleType(str, Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    TRUCK = "TRUCK"
    BUS = "BUS"
    VAN = "VAN"
    COUPE = "COUPE"
    HATCHBACK = "HATCHBACK"