from fastapi import status
import pytest
from datetime import datetime
from models import FoodItem, MealLog

def test_seed_and_get_foods(client, session):
    # Check if empty, add seed data using session directly
    foods = session.query(FoodItem).all()
    if not foods:
        session.add(FoodItem(name="Test Apple", calories=50, protein=0, carbs=10, fats=0, is_custom=False))
        session.commit()

    response = client.get("/foods")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    
    # Test Search
    session.add(FoodItem(name="UniqueFoodXYZ", calories=100, protein=10, carbs=10, fats=2, is_custom=False))
    session.commit()
    
    response = client.get("/foods?search=UniqueFoodXYZ")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "UniqueFoodXYZ"

def test_create_custom_food(client, auth_headers):
    new_food = {
        "name": "My Custom Cake",
        "calories": 500,
        "protein": 5,
        "carbs": 80,
        "fats": 20,
        "is_custom": True
    }
    response = client.post("/foods", json=new_food, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "My Custom Cake"
    assert data["is_custom"] is True

def test_log_meal_and_history(client, auth_headers):
    meal_data = {
        "date": datetime.utcnow().isoformat(),
        "meal_type": "breakfast",
        "food_item": {
            "name": "Oatmeal",
            "calories": 150,
            "protein": 5,
            "carbs": 25,
            "fats": 2,
            "is_custom": False,
            "id": 123 
        }
    }
    
    # Log Meal
    response = client.post("/meals", json=meal_data, headers=auth_headers)
    if response.status_code == 422:
        print(response.json())
        
    assert response.status_code == status.HTTP_200_OK
    
    # Get History
    response = client.get("/meals/history", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    # Check snapshot data
    assert data[0]["food_snapshot"]["name"] == "Oatmeal"

def test_analytics_summary(client, auth_headers, session, test_user):
    # Clear previous meals for this user
    # test_user is an object now
    session.query(MealLog).filter(MealLog.user_id == test_user.id).delete()
    session.commit()
    
    # Log 2 meals today
    today = datetime.utcnow().isoformat()
    client.post("/meals", json={
        "date": today,
        "meal_type": "lunch",
        "food_item": {"name": "A", "calories": 100, "protein": 10, "carbs": 10, "fats": 0}
    }, headers=auth_headers)
    
    client.post("/meals", json={
        "date": today,
        "meal_type": "dinner",
        "food_item": {"name": "B", "calories": 200, "protein": 20, "carbs": 20, "fats": 0}
    }, headers=auth_headers)
    
    response = client.get("/analytics/summary", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["today"]["calories"] == 300
    assert data["today"]["protein"] == 30
    assert "goal" in data
