from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal

from app.models.enums import (
    UserRole,
    VehicleType,
)

from app.models.service_package import ServicePackage
from app.models.service_package_price import ServicePackagePrice
from app.models.user import User


db: Session = SessionLocal()


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    role: UserRole,
):

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        print(f"✔ {role.value}: {email} already exists")
        return existing

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        password_hash=hash_password("Password123!"),
        role=role,
        is_active=True,
        email_verified=True,
        phone_verified=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✅ Created {role.value}: {email}")

    return user


def seed_users():

    create_user(
        "Super",
        "Admin",
        "superadmin@mcw.com",
        "08000000001",
        UserRole.SUPER_ADMIN,
    )

    create_user(
        "System",
        "Admin",
        "admin@mcw.com",
        "08000000002",
        UserRole.ADMIN,
    )

    create_user(
        "John",
        "Dispatcher",
        "dispatcher@mcw.com",
        "08000000003",
        UserRole.DISPATCHER,
    )

    create_user(
        "James",
        "Washer",
        "washer1@mcw.com",
        "08000000004",
        UserRole.WASHER,
    )

    create_user(
        "David",
        "Washer",
        "washer2@mcw.com",
        "08000000005",
        UserRole.WASHER,
    )


PACKAGE_DATA = [

    {
        "name": "Basic Wash",
        "description": "Exterior wash and quick interior wipe.",
        "duration": 40,
        "prices": {
            VehicleType.SEDAN: 7000,
            VehicleType.SUV: 9000,
            VehicleType.TRUCK: 12000,
            VehicleType.BUS: 15000,
            VehicleType.VAN: 11000,
            VehicleType.COUPE: 7000,
            VehicleType.HATCHBACK: 6500,
        },
    },

    {
        "name": "Premium Wash",
        "description": "Exterior wash, tyre shine and interior cleaning.",
        "duration": 60,
        "prices": {
            VehicleType.SEDAN: 10000,
            VehicleType.SUV: 13000,
            VehicleType.TRUCK: 17000,
            VehicleType.BUS: 20000,
            VehicleType.VAN: 15000,
            VehicleType.COUPE: 10000,
            VehicleType.HATCHBACK: 9000,
        },
    },

    {
        "name": "Deluxe Wash",
        "description": "Premium wash with waxing.",
        "duration": 90,
        "prices": {
            VehicleType.SEDAN: 15000,
            VehicleType.SUV: 18000,
            VehicleType.TRUCK: 22000,
            VehicleType.BUS: 26000,
            VehicleType.VAN: 21000,
            VehicleType.COUPE: 15000,
            VehicleType.HATCHBACK: 14000,
        },
    },

    {
        "name": "Interior Detailing",
        "description": "Deep interior detailing.",
        "duration": 120,
        "prices": {
            VehicleType.SEDAN: 18000,
            VehicleType.SUV: 22000,
            VehicleType.TRUCK: 28000,
            VehicleType.BUS: 32000,
            VehicleType.VAN: 26000,
            VehicleType.COUPE: 18000,
            VehicleType.HATCHBACK: 17000,
        },
    },

    {
        "name": "Full Detailing",
        "description": "Complete interior and exterior detailing.",
        "duration": 180,
        "prices": {
            VehicleType.SEDAN: 25000,
            VehicleType.SUV: 30000,
            VehicleType.TRUCK: 40000,
            VehicleType.BUS: 50000,
            VehicleType.VAN: 36000,
            VehicleType.COUPE: 25000,
            VehicleType.HATCHBACK: 22000,
        },
    },

]
def seed_packages():

    for item in PACKAGE_DATA:

        package = (
            db.query(ServicePackage)
            .filter(
                ServicePackage.name == item["name"]
            )
            .first()
        )

        if package is None:

            package = ServicePackage(
                name=item["name"],
                description=item["description"],
                estimated_duration=item["duration"],
                is_active=True,
            )

            db.add(package)
            db.flush()

            print(f"✅ Created package: {package.name}")

        else:

            print(f"✔ Package already exists: {package.name}")

        for vehicle_type, amount in item["prices"].items():

            existing_price = (
                db.query(ServicePackagePrice)
                .filter(
                    ServicePackagePrice.service_package_id == package.id,
                    ServicePackagePrice.vehicle_type == vehicle_type,
                )
                .first()
            )

            if existing_price:

                continue

            db.add(
                ServicePackagePrice(
                    service_package_id=package.id,
                    vehicle_type=vehicle_type,
                    price=amount,
                    is_active=True,
                )
            )

            print(
                f"   ↳ {vehicle_type.value}: ₦{amount:,}"
            )

    db.commit()


def main():

    try:

        print("\n==============================")
        print("SEEDING DATABASE")
        print("==============================\n")

        seed_users()

        seed_packages()

        db.commit()

        print("\n==============================")
        print("✅ DATABASE SEEDED SUCCESSFULLY")
        print("==============================\n")

    except Exception as e:

        db.rollback()

        print("\n==============================")
        print("❌ SEED FAILED")
        print("==============================")
        print(e)
        print("==============================\n")

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()