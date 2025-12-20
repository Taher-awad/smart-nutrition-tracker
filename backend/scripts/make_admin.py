import sys
import os

# Add backend directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import select
from database import get_session, create_db_and_tables
from models import User

def make_admin(email: str):
    # Ensure tables exist
    create_db_and_tables()
    
    with next(get_session()) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        
        if not user:
            print(f"User with email '{email}' not found.")
            return
        
        user.is_admin = True
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Successfully promoted {user.full_name} ({user.email}) to Admin!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <email>")
    else:
        make_admin(sys.argv[1])
