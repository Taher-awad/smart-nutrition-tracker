import requests
import sys

BASE_URL = "http://localhost:8001"
EMAIL = "test@example.com"
PASSWORD = "password"

def run_test(name, func):
    print(f"--- Testing {name} ---")
    try:
        func()
        print(f"✅ {name} Passed\n")
    except Exception as e:
        print(f"❌ {name} Failed: {e}\n")

def get_token():
    response = requests.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
    if response.status_code != 200:
        # Try registering first
        print("Login failed, trying to register...")
        reg_response = requests.post(f"{BASE_URL}/users/", json={"email": EMAIL, "password": PASSWORD, "full_name": "Test User"})
        if reg_response.status_code not in [200, 400]:
            raise Exception(f"Registration failed: {reg_response.text}")
        
        # Login again
        response = requests.post(f"{BASE_URL}/token", data={"username": EMAIL, "password": PASSWORD})
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.text}")
    
    return response.json()["access_token"]

token = None

def test_auth():
    global token
    token = get_token()
    print(f"Got Token: {token[:10]}...")

def test_profile():
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "age": 25,
        "gender": "male",
        "height": 180,
        "weight": 75,
        "activity_level": "moderate",
        "goal": "lose"
    }
    response = requests.put(f"{BASE_URL}/users/profile", json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Profile update failed: {response.text}")
    user = response.json()
    print(f"Profile Updated. Daily Calorie Goal: {user.get('daily_calorie_goal')}")

def test_foods():
    response = requests.get(f"{BASE_URL}/foods")
    if response.status_code != 200:
        raise Exception(f"Get foods failed: {response.text}")
    foods = response.json()
    print(f"Found {len(foods)} foods")

def test_log_meal():
    headers = {"Authorization": f"Bearer {token}"}
    # Get a food first
    foods = requests.get(f"{BASE_URL}/foods").json()
    if not foods:
        raise Exception("No foods found to log")
    food = foods[0]
    
    data = {
        "user_id": "ignored",
        "food_item": food,
        "date": "2023-10-27T10:00:00",
        "meal_type": "snack"
    }
    response = requests.post(f"{BASE_URL}/meals", json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Log meal failed: {response.text}")
    print("Meal logged successfully")

def test_generate_plan():
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/plans/generate", headers=headers)
    if response.status_code != 200:
        raise Exception(f"Generate plan failed: {response.text}")
    plan = response.json()
    print(f"Generated plan for {len(plan['meals'])} meals")

def test_analytics():
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/analytics/summary", headers=headers)
    if response.status_code != 200:
        raise Exception(f"Analytics failed: {response.text}")
    data = response.json()
    print(f"Analytics: {data}")

if __name__ == "__main__":
    run_test("Auth", test_auth)
    run_test("Profile Update", test_profile)
    run_test("Get Foods", test_foods)
    run_test("Log Meal", test_log_meal)
    run_test("Generate Plan", test_generate_plan)
    run_test("Analytics", test_analytics)
