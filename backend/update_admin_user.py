#!/usr/bin/env python3

from sqlalchemy import text

from app.core.database import get_write_db  # type: ignore[attr-defined]
from app.models.user import User


def update_admin_user() -> None:
    """Add is_admin column and update admin user"""
    try:
        db = next(get_write_db())  # type: ignore[name-defined]

        try:
            db.execute(
                text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE")
            )
            db.commit()
            print("✅ Added is_admin column to users table")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️  is_admin column already exists")
            else:
                print(f"⚠️  Error adding column: {e}")
            db.rollback()

        admin_user = (
            db.query(User).filter(User.email == "aadish.bahati@echostor.com").first()
        )

        if admin_user:
            admin_user.is_admin = True
            db.commit()
            print(f"✅ Updated admin user {admin_user.email} with is_admin = True")

            updated_user = (
                db.query(User)
                .filter(User.email == "aadish.bahati@echostor.com")
                .first()
            )
            print(
                f"✅ Verification: {updated_user.email} is_admin = {updated_user.is_admin}"
            )
        else:
            print("❌ Admin user not found")

        db.close()

    except Exception as e:
        print(f"❌ Error updating admin user: {e}")


if __name__ == "__main__":
    update_admin_user()
