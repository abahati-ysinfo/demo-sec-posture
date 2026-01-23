#!/usr/bin/env python3

import getpass
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uuid

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User


def create_admin_user() -> None:
    """Create admin user with secure password input"""
    admin_email = input("Enter admin email: ").strip()
    if not admin_email:
        print("Email cannot be empty")
        return

    admin_password = getpass.getpass("Enter admin password: ")
    if not admin_password:
        print("Password cannot be empty")
        return

    admin_name = input("Enter admin full name: ").strip()
    if not admin_name:
        admin_name = "Admin User"

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if existing_admin:
            print("Admin user already exists")
            return

        admin_user = User(
            id=str(uuid.uuid4()),
            email=admin_email,
            full_name=admin_name,
            company_name="EchoStor",
            password_hash=get_password_hash(admin_password),
            is_active=True,
        )

        db.add(admin_user)
        db.commit()
        print(f"Admin user created successfully with ID: {admin_user.id}")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
