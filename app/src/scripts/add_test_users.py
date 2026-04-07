from core.database import SessionLocal  # Import your actual session factory
from services.user_service import UserService


def seed_test_users():
    # 1. Setup the DB session and Service
    db = SessionLocal()
    user_service = UserService(db)

    # 2. Define the test data
    test_users = [
        {
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Vite",
            "validation_code": "code_123_abc",
        },
        {
            "email": "bob@example.com",
            "first_name": "Bob",
            "last_name": "React",
            "validation_code": "code_456_def",
        },
        {
            "email": "charlie@example.com",
            "first_name": "Charlie",
            "last_name": "Python",
            "validation_code": "code_789_ghi",
        },
    ]

    print("--- Starting User Seed Process ---")

    for user_data in test_users:
        try:
            # Attempt to create the user
            new_user = user_service.create_user(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                validation_code=user_data["validation_code"],
            )
            print(f"✅ Success: Created user {new_user.email}")

        except ValueError as e:
            # This blocks the creation and prints the error message from the service
            print(f"❌ Blocked: {e}")

        except Exception as e:
            print(f"⚠️ Unexpected Error for {user_data['email']}: {e}")

    db.close()
    print("--- Seed Process Complete ---")


if __name__ == "__main__":
    seed_test_users()
