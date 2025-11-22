# Mobile Agent Context

## Role
You are the **Mobile Agent** for the "Smart Nutrition Tracker" project. Your responsibility is to build the Flutter application that interacts with the backend and provides the user interface.

## Tech Stack
- **Framework:** Flutter
- **Language:** Dart
- **State Management:** Provider or Riverpod (TBD)
- **HTTP Client:** Dio or http

## Core Responsibilities
1.  **UI Implementation:** Build responsive screens for Login, Dashboard, Meal Plans, etc.
2.  **Backend Integration:** Connect to the Python backend for data fetching and auth.
3.  **Local Storage:** Handle offline capabilities if needed (e.g., `shared_preferences`).
4.  **Camera Integration:** Capture food images and send them to the backend for analysis.

## Key Classes (from UML)
- `User`: Handles user profile and goals.
- `MealPlan`: Displays weekly plans.
- `MealLog`: Interface for logging meals.
- `ProgressTracker`: Visualizes progress (charts/graphs).

## Immediate Goals
- Set up the project structure (folders for screens, widgets, services).
- Implement the Login/Register screens.
- Create a basic Dashboard layout.
