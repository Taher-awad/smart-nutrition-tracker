from repositories.user_repository import UserRepository
from database import get_database

repo = UserRepository()
email = "taher@gmail.com"
user = repo.get_by_email(email)

if user:
    repo.delete_one({"email": email})
    print(f"Deleted user: {email}")
else:
    print(f"User not found: {email}")
