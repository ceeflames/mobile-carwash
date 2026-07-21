from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    WASHER = "WASHER"
    DISPATCHER = "DISPATCHER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class WasherAvailability(str, Enum):
    AVAILABLE = "AVAILABLE"
    BUSY = "BUSY"
    OFFLINE = "OFFLINE"
    ON_BREAK = "ON_BREAK"


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
    ACCEPTED = "ACCEPTED"
    ARRIVED = "ARRIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    WASHING = "WASHING"
    NO_SHOW = "NO_SHOW"
    REJECTED = "REJECTED"
    ON_THE_WAY = "ON_THE_WAY"
    ASSIGNED = "ASSIGNED"



class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class PaymentProvider(str, Enum):
    PAYSTACK = "PAYSTACK"
    FLUTTERWAVE = "FLUTTERWAVE"