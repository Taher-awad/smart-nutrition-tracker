from fastapi import status
import pytest
from models import User

def test_update_profile_and_bmr_calculation(client, auth_headers, session, test_user):
    # Initial check (assuming logic in main.py is correct, TDEE for test_user should be specific)
    # Male, 80kg, 180cm, 30y, moderate (1.55), lose (-500)
    # BMR = (10*80) + (6.25*180) - (5*30) + 5 = 800 + 1125 - 150 + 5 = 1780
    # TDEE = 1780 * 1.55 = 2759
    # Goal = 2759 - 500 = 2259
    
    # Let's update to specific values to test calculation logic
    # Note: test_user is an object.
    
    update_data = {
        "gender": "male",
        "weight": 100,
        "height": 180,
        "age": 30,
        "activity_level": "sedentary", # 1.2
        "goal": "maintain" # +0
    }
    # BMR = (10*100) + (6.25*180) - (5*30) + 5 = 1000 + 1125 - 150 + 5 = 1980
    # TDEE = 1980 * 1.2 = 2376
    # Goal = 2376
    
    response = client.put("/users/profile", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["weight"] == 100
    assert data["daily_calorie_goal"] == 2376.0
    
    # Verify DB persistence
    # Use session to get user
    session.refresh(test_user) # Refresh instance from DB
    assert test_user.weight == 100
    assert test_user.daily_calorie_goal == 2376.0
