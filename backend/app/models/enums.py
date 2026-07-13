from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    WASHER = "washer"
    DISPATCHER = "dispatcher"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class VehicleType(str, Enum):
    SEDAN = "SEDAN"
    SUV = "SUV"
    TRUCK = "TRUCK"
    BUS = "BUS"
    VAN = "VAN"
    COUPE = "COUPE"
    HATCHBACK = "HATCHBACK"