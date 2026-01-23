#!/usr/bin/env python3
"""Check if admin user exists in database"""

from app.core.database import SessionLocal
from app.models.user import User


def check_admin_user() -> None:
    """Check if admin user exists in database"""
    try:
        db = SessionLocal()

        admin_user = (
            db.query(User).filter(User.email == "aadish.bahati@echostor.com").first()
        )

        if admin_user:
            print("✅ Admin user found:")
            print(f"   Email: {admin_user.email}")
            print(f"   Name: {admin_user.full_name}")
            print(f"   Is Admin: {admin_user.is_admin}")
            print(f"   User ID: {admin_user.id}")
            print(f"   Created: {admin_user.created_at}")
        else:
            print("❌ No admin user found in database")

        all_users = db.query(User).all()
        print(f"\n📊 Total users in database: {len(all_users)}")
        for user in all_users:
            print(f"   - {user.email} (admin: {user.is_admin})")

        db.close()

    except Exception as e:
        print(f"❌ Error checking admin user: {e}")


if __name__ == "__main__":
    check_admin_user()
