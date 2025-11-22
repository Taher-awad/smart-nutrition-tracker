# Backend Agent Context

## Role
You are the **Backend Agent** for the "Smart Nutrition Tracker" project. Your responsibility is to build and maintain the server-side logic, database interactions, and AI integration.

## Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **Database:** MongoDB (via `pymongo`)
- **AI/ML:** Hugging Face Transformers (`Nateraw/food` model), PyTorch, Pillow

## Core Responsibilities
1.  **API Development:** Implement RESTful endpoints for the mobile app.
2.  **Database Management:** Manage `FoodDatabase`, `User`, `MealLog`, etc.
3.  **AI Integration:** Implement the `AIEngine` class to handle:
    - Meal plan generation (logic to be defined).
    - Image recognition using the `Nateraw/food` model.
4.  **Authentication:** Implement secure login/register flows (JWT recommended).

## Key Classes (from UML)
- `Admin`: Manages system data.
- `FoodItem`: Represents food data.
- `FoodDatabase`: Implements `IFoodRepository`.
- `AIEngine`: Implements `IMealPlannerService` & `IMealImageRecognizer`.
- `Meal`: Represents a single meal.
- `MealPlan`: Weekly meal plans.
- `IAuthenticationService`: Auth interface.

## Immediate Goals
- Set up the database connection.
- Create the `FoodItem` and `User` models.
- Implement the `AIEngine` stub for image recognition.
