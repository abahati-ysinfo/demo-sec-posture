#!/usr/bin/env python3
"""
Production admin setup script
Creates admin user in database and provides environment variables for deployment
"""

import os
import secrets
import string
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uuid

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User


def generate_secure_password(length: int = 16) -> str:
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def setup_production_admin() -> None:
    """Set up admin user for production deployment"""
    admin_email = "admin@administrator.com"
    admin_password = generate_secure_password()
    admin_name = "Administrator"

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if existing_admin:
            existing_admin.is_admin = True  # type: ignore[assignment]
            db.commit()
            print(f"✅ Updated existing user {admin_email} with admin privileges")
            print("🔑 Use existing password or reset via admin panel")
            return

        admin_user = User(
            id=str(uuid.uuid4()),
            email=admin_email,
            full_name=admin_name,
            company_name="Security Posture",
            password_hash=get_password_hash(admin_password),
            is_active=True,
            is_admin=True,
        )

        db.add(admin_user)
        db.commit()

        print("✅ Admin user created successfully!")
        print(f"📧 Email: {admin_email}")
        print(f"🔑 Password: {admin_password}")
        print(f"🆔 User ID: {admin_user.id}")
        print("\n⚠️  IMPORTANT: Save these credentials securely!")

    except Exception as e:
        print(f"❌ Error setting up admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    setup_production_admin()
