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

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    WASHER_ASSIGNED = "WASHER_ASSIGNED"
    ACCEPTED = "ACCEPTED"
    EN_ROUTE = "EN_ROUTE"
    ARRIVED = "ARRIVED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"