from datetime import datetime, timedelta
from decimal import Decimal
import random

from faker import Faker

from app.db.session import SessionLocal
from app.core.security import hash_password

from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.address import Address
from app.models.booking import Booking
from app.models.booking_status_history import BookingStatusHistory
from app.models.service_package_price import ServicePackagePrice

from app.models.enums import (
    UserRole,
    VehicleType,
    BookingStatus,
    PaymentStatus,
)

fake = Faker()


def booking_reference():
    return f"CW-{random.randint(100000,999999)}"


def random_booking_status():
    return random.choice(
        [
            BookingStatus.PENDING,
            BookingStatus.WASHER_ASSIGNED,
            BookingStatus.ACCEPTED,
            BookingStatus.EN_ROUTE,
            BookingStatus.ARRIVED,
            BookingStatus.IN_PROGRESS,
            BookingStatus.COMPLETED,
        ]
    )


def seed_demo_data():

    print("\n========== DEMO DATA ==========\n")

    db = SessionLocal()

    try:

        dispatcher = (
            db.query(User)
            .filter(User.role == UserRole.DISPATCHER)
            .first()
        )

        if dispatcher is None:
            raise Exception(
                "No dispatcher found. Run seed_database.py first."
            )

        washers = (
            db.query(User)
            .filter(User.role == UserRole.WASHER)
            .all()
        )

        if not washers:
            raise Exception(
                "No washers found. Run seed_database.py first."
            )

        package_prices = (
            db.query(ServicePackagePrice)
            .all()
        )

        if not package_prices:
            raise Exception(
                "No service package prices found."
            )

        customers = []
        addresses = []
        vehicles = []
        bookings = []

        print("Creating customers...")

        for i in range(10):

            customer = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=f"customer{i}@demo.com",
                phone=f"0803000{i:04}",
                password_hash=hash_password(
                    "Password123!"
                ),
                role=UserRole.CUSTOMER,
                is_active=True,
                email_verified=True,
                phone_verified=True,
            )

            db.add(customer)
            customers.append(customer)

        db.flush()

        print(f"{len(customers)} customers created.")
        print("Creating addresses...")

        for customer in customers:

            address = Address(
                user_id=customer.id,
                title="Home",
                street_address=fake.street_address(),
                city="Abuja",
                state="FCT",
                landmark=fake.street_name(),
                additional_notes="Demo customer address",
                latitude=9.0765,
                longitude=7.3986,
                is_default=True,
            )

            db.add(address)
            addresses.append(address)

        db.flush()

        print(f"{len(addresses)} addresses created.")

        print("Creating vehicles...")

        vehicle_catalog = [
            ("Toyota", "Corolla", VehicleType.SEDAN),
            ("Toyota", "Prado", VehicleType.SUV),
            ("Honda", "Accord", VehicleType.SEDAN),
            ("Lexus", "RX350", VehicleType.SUV),
            ("Hyundai", "Elantra", VehicleType.SEDAN),
            ("Mercedes", "Sprinter", VehicleType.VAN),
            ("Ford", "Transit", VehicleType.VAN),
            ("Peugeot", "508", VehicleType.SEDAN),
            ("Kia", "Sportage", VehicleType.SUV),
            ("Nissan", "Navara", VehicleType.TRUCK),
        ]

        for index, customer in enumerate(customers):

            make, model, vehicle_type = random.choice(
                vehicle_catalog
            )

            vehicle = Vehicle(
                owner_id=customer.id,
                make=make,
                model=model,
                year=random.randint(2018, 2025),
                color=random.choice(
                    [
                        "Black",
                        "White",
                        "Silver",
                        "Blue",
                        "Grey",
                        "Red",
                    ]
                ),
                plate_number=f"ABC-{1000 + index}",
                vehicle_type=vehicle_type,
                is_default=True,
            )

            db.add(vehicle)
            vehicles.append(vehicle)

        db.flush()

        print(f"{len(vehicles)} vehicles created.")

        print("Creating bookings...")

        for _ in range(20):

            customer = random.choice(customers)

            vehicle = next(
                v
                for v in vehicles
                if v.owner_id == customer.id
            )

            address = next(
                a
                for a in addresses
                if a.user_id == customer.id
            )

            washer = random.choice(washers)

            matching_prices = [
                price
                for price in package_prices
                if price.vehicle_type
                == vehicle.vehicle_type
            ]

            if not matching_prices:
                matching_prices = package_prices

            selected_price = random.choice(
                matching_prices
            )

            booking = Booking(
                booking_reference=booking_reference(),
                customer_id=customer.id,
                vehicle_id=vehicle.id,
                address_id=address.id,
                service_package_id=selected_price.service_package_id,
                service_package_price_id=selected_price.id,
                washer_id=washer.id,
                dispatcher_id=dispatcher.id,
                scheduled_at=datetime.utcnow() + timedelta(
                    days=random.randint(0, 7),
                    hours=random.randint(8, 17),
                ),
                status=random_booking_status(),
                payment_status=random.choice(
                    [
                        PaymentStatus.PENDING,
                        PaymentStatus.PAID,
                    ]
                ),
                final_price=Decimal(selected_price.price),
                customer_note=fake.sentence(),
                cancelled_reason=None,
            )

            db.add(booking)
            bookings.append(booking)

        db.flush()

        print(f"{len(bookings)} bookings created.")

        print("Creating booking status history...")

        for booking in bookings:

            first_history = BookingStatusHistory(
                booking_id=booking.id,
                from_status=None,
                to_status=BookingStatus.PENDING,
                changed_by_id=dispatcher.id,
                reason="Booking created",
                old_scheduled_at=None,
                new_scheduled_at=booking.scheduled_at,
            )

            db.add(first_history)

            if booking.status != BookingStatus.PENDING:

                second_history = BookingStatusHistory(
                    booking_id=booking.id,
                    from_status=BookingStatus.PENDING,
                    to_status=booking.status,
                    changed_by_id=dispatcher.id,
                    reason="Demo status progression",
                    old_scheduled_at=booking.scheduled_at,
                    new_scheduled_at=booking.scheduled_at,
                )

                db.add(second_history)

        db.flush()

        print("Booking history created.")

        db.commit()

        print()
        print("=" * 60)
        print("🎉 DEMO DATA SEEDED SUCCESSFULLY")
        print("=" * 60)
        print(f"Customers : {len(customers)}")
        print(f"Addresses : {len(addresses)}")
        print(f"Vehicles  : {len(vehicles)}")
        print(f"Bookings  : {len(bookings)}")
        print("=" * 60)

    except Exception as e:

        db.rollback()

        print()
        print("=" * 60)
        print("❌ DEMO DATA SEED FAILED")
        print("=" * 60)
        print(e)
        print("=" * 60)

        raise

    finally:

        db.close()


if __name__ == "__main__":
    seed_demo_data()
