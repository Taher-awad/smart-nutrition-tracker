import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from database import get_session, create_db_and_tables
from models import User
from services.auth_service import AuthenticationService

def create_admin_user():
    create_db_and_tables()
    auth_service = AuthenticationService()
    email = "admin@admin.com"
    password = "admin"
    
    with next(get_session()) as session:
        # Check if exists
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        
        if user:
            print(f"User {email} already exists. Updating to Admin...")
            user.is_admin = True
            user.hashed_password = auth_service.get_password_hash(password) # Reset password to 'admin'
            session.add(user)
        else:
            print(f"Creating new Admin user: {email}")
            hashed_pw = auth_service.get_password_hash(password)
            user = User(
                email=email,
                hashed_password=hashed_pw,
                full_name="System Admin",
                is_admin=True,
                is_active=True
            )
            session.add(user)
            
        session.commit()
        session.refresh(user)
        print(f"DONE. User: {user.email}, Password: {password}, Admin: {user.is_admin}")

if __name__ == "__main__":
    try:
        create_admin_user()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
