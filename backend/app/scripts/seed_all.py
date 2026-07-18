from app.scripts.seed_database import seed_database
from app.scripts.seed_demo_data import seed_demo_data


def main():
    seed_database()
    seed_demo_data()

    print("\nDatabase seeded successfully.")


if __name__ == "__main__":
    main()