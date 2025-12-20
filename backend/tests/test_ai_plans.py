from fastapi import status
import pytest
from datetime import datetime, timedelta

def test_recognize_image(client, auth_headers):
    # Mock AI Service returns a random food or fixed one
    # We don't really upload an image here (endpoint mock implementation doesn't use the body yet?)
    # Let's check api. It expects nothing in body? Or File?
    # backend/main.py: async def recognize_food_image(...)
    # It takes no body parameters in the signature !?
    # Just depends(current_user) and ai_service.
    # So a POST to /ai/recognize with auth headers should work.
    
    response = client.post("/ai/recognize", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "name" in data
    assert "calories" in data

def test_generate_meal_plan(client, auth_headers):
    response = client.post("/plans/generate", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "meals" in data
    assert len(data["meals"]) > 0
    # Check structure of a planned meal
    first_meal = data["meals"][0]
    assert "meal_type" in first_meal
    assert "food" in first_meal
    assert "date" in first_meal
