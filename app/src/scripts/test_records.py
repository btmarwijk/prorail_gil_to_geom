from datetime import datetime

# Import your DB session and models
from core.database import SessionLocal
from models import Group, Organization, Project, User
from models.enums import UserRole
from sqlalchemy import select


def seed_test_users():
    # Initialize the session
    db = SessionLocal()

    print("--- Starting User Seeding ---")

    try:
        for role in UserRole:
            email = f"test_{role.value}@example.com"

            # Check if user already exists
            existing_user = db.execute(
                select(User).where(User.email == email)
            ).scalar_one_or_none()

            if not existing_user:
                new_user = User(
                    role=role,
                    email=email,
                    first_name="Test",
                    last_name=role.name.title().replace("_", " "),
                    created_at=datetime.utcnow(),
                )
                db.add(new_user)
                print(f"✅ Created: {role.value} ({email})")
            else:
                print(f"⏭️  Skipped: {role.value} (Already exists)")

        # Commit all changes at once
        db.commit()
        print("--- Seeding Complete ---")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


def seed_test_organizations():
    db = SessionLocal()
    print("--- Starting Organization Seeding ---")

    orgs_to_create = [
        {"name": "ProRail Maintenance", "slug": "prorail-maint"},
        {"name": "Asset Management NL", "slug": "asset-mgmt-nl"},
    ]

    try:
        for org_data in orgs_to_create:
            existing = db.execute(
                select(Organization).where(Organization.slug == org_data["slug"])
            ).scalar_one_or_none()

            if not existing:
                new_org = Organization(
                    name=org_data["name"], slug=org_data["slug"], is_activate=True
                )
                db.add(new_org)
                print(f"✅ Created Org: {org_data['name']}")
            else:
                print(f"⏭️  Skipped Org: {org_data['name']} (Exists)")

        db.commit()
    except Exception as e:
        print(f"❌ Org Error: {e}")
        db.rollback()
    finally:
        db.close()


def seed_test_projects():
    db = SessionLocal()
    print("--- Starting Project Seeding ---")

    try:
        # Get first available organization
        org = db.execute(select(Organization)).scalars().first()
        if not org:
            print("❌ No Organization found. Seed orgs first!")
            return

        projects = ["Betuweroute Phase 1", "Utrecht Central Upgrade"]

        for p_name in projects:
            existing = db.execute(
                select(Project).where(Project.project_naam == p_name)
            ).scalar_one_or_none()

            if not existing:
                new_project = Project(
                    project_naam=p_name,
                    organization_id=org.id,
                    created_at=datetime.utcnow(),
                )
                db.add(new_project)
                print(f"✅ Created Project: {p_name}")

        db.commit()
    except Exception as e:
        print(f"❌ Project Error: {e}")
        db.rollback()
    finally:
        db.close()


def seed_test_groups():
    db = SessionLocal()
    print("--- Starting Group Seeding ---")

    try:
        # Get first admin user and first org
        admin = (
            db.execute(select(User).where(User.role == UserRole.ADMIN))
            .scalars()
            .first()
        )
        org = db.execute(select(Organization)).scalars().first()

        if not admin or not org:
            print("❌ Missing User or Org. Seed them first!")
            return

        group_names = ["Infrastructure Team", "Safety Oversight"]

        for g_name in group_names:
            existing = db.execute(
                select(Group).where(Group.name == g_name)
            ).scalar_one_or_none()

            if not existing:
                new_group = Group(
                    name=g_name, creator_id=admin.id, organization_id=org.id
                )
                db.add(new_group)
                print(f"✅ Created Group: {g_name}")

        db.commit()
    except Exception as e:
        print(f"❌ Group Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_test_users()  # 1. Users first (needed for Group creator_id)
    seed_test_organizations()  # 2. Orgs second (needed for Project/Group)
    seed_test_projects()  # 3. Projects
    seed_test_groups()  # 4. Groups
