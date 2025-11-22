# Smart Nutrition Tracker

A full-stack nutrition tracking application with a FastAPI backend and Flutter mobile frontend. Track your calories, macronutrients, meals, and get personalized nutrition insights.

## 🌟 Features

### Backend (FastAPI)
- **JWT Authentication** with Argon2 password hashing
- **Rate Limiting** (5 login attempts/min, 3 registration attempts/min)
- **BMR/TDEE Calculation** using Mifflin-St Jeor equation
- **Food Database** with search functionality
- **Meal Logging** with timestamps
- **Weekly Meal Planning** (auto-generates 21 meals)
- **Nutrition Analytics** dashboard
- **Mock AI Image Recognition**
- **Structured Logging** with Loguru
- **CORS Support** for web clients

### Mobile (Flutter)
- **Modern UI** with Material Design 3 and custom theme
- **5 Interactive Charts**:
  - Calorie progress ring
  - Weekly calorie trend line chart
  - Macro distribution pie chart
  - Nutrient progress bars
  - Water intake tracker
- **Profile Management** with Settings page
- **Meal Logging** with food search
- **Weekly Meal Planner** with grocery list
- **Persistent Login** with token storage
- **Smart Navigation** (auto-skip profile setup if data exists)

## 📋 Prerequisites

### Backend
- Python 3.11 or higher
- Docker (for MongoDB)
- pip and venv

### Mobile
- Flutter SDK 3.0 or higher
- For Android: Android Studio with SDK
- For Web: Chrome or Firefox browser

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Taher-awad/smart-nutrition-tracker.git
cd smart-nutrition-tracker
```

---

## 🖥️ Backend Setup & Installation

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Start MongoDB with Docker

```bash
docker-compose up -d
```

This will start MongoDB on port 27017. Verify it's running:
```bash
docker ps
```

### Step 6: Configure Environment Variables

The `.env` file is already configured with secure defaults. You can modify it if needed:

```bash
# backend/.env
SECRET_KEY=your-super-secret-key-change-this-in-production
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=nutrition_tracker
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 7: Run the Backend Server

```bash
uvicorn main:app --reload --port 8001
```

The backend API will be available at:
- **API**: http://localhost:8001
- **Swagger Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Verify Backend is Running

Open http://localhost:8001/docs in your browser. You should see the Swagger UI with all available endpoints.

---

## 📱 Mobile App Setup & Installation

### Step 1: Navigate to Mobile Directory

```bash
cd mobile
```

### Step 2: Install Flutter Dependencies

```bash
flutter pub get
```

---

## 🌐 Running Flutter App for Web

### Step 1: Check Available Devices

```bash
flutter devices
```

You should see `web-server` or `chrome` in the list.

### Step 2: Run on Web Server

**Development Mode (Hot Reload):**
```bash
flutter run -d web-server --web-port 8080
```

**Or run on Chrome:**
```bash
flutter run -d chrome
```

### Step 3: Access the App

Open your browser and navigate to:
- http://localhost:8080

### Production Web Build (Fast Performance)

For much faster performance, build a production version:

```bash
flutter build web --release
python3 -m http.server 8080 --directory build/web
```

Then open http://localhost:8080

**Note**: Production builds are 10-20x faster than debug builds!

---

## 📲 Running Flutter App for Android

### Prerequisites
- Android Studio installed
- Android SDK configured
- USB debugging enabled on your device OR Android emulator running

### Step 1: Check Connected Devices

```bash
flutter devices
```

You should see your Android device or emulator in the list.

### Step 2: Run on Android Device/Emulator

**Debug Mode:**
```bash
flutter run
```

Flutter will automatically detect and run on the connected Android device.

**Or specify the device:**
```bash
flutter run -d <device-id>
```

### Step 3: Build APK (Release)

To create a release APK for distribution:

```bash
flutter build apk --release
```

The APK will be located at:
```
mobile/build/app/outputs/flutter-apk/app-release.apk
```

### Step 4: Install on Device

Transfer the APK to your Android device and install it, or use:

```bash
flutter install
```

### Troubleshooting Android

If you encounter issues:

```bash
# Check Flutter setup
flutter doctor

# Accept Android licenses
flutter doctor --android-licenses

# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

---

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env` for environment-specific settings:

```env
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=nutrition_tracker
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Mobile Configuration

Edit `mobile/lib/services/api_service.dart` to change the API URL:

```dart
static const String baseUrl = 'http://127.0.0.1:8001'; // For Web/Emulator
// static const String baseUrl = 'http://10.0.2.2:8001'; // For Android Emulator
// static const String baseUrl = 'http://YOUR_IP:8001'; // For Physical Device
```

---

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Key Endpoints

- `POST /users/` - Register new user
- `POST /token` - Login and get JWT token
- `PUT /users/profile` - Update user profile
- `GET /foods` - Search food database
- `POST /meals` - Log a meal
- `POST /plans/generate` - Generate weekly meal plan
- `GET /analytics/summary` - Get nutrition analytics

---

## 🧪 Testing

### Test Backend API

```bash
cd backend
source venv/bin/activate
python verify_api.py
```

### Test with Swagger UI

1. Open http://localhost:8001/docs
2. Click "POST /users/" to register
3. Click "POST /token" to login and get a token
4. Click "Authorize" and enter: `Bearer YOUR_TOKEN`
5. Try other endpoints

---

## 🎯 Usage Guide

### First Time Setup

1. **Start Backend**:
   ```bash
   cd backend
   docker-compose up -d
   source venv/bin/activate
   uvicorn main:app --reload --port 8001
   ```

2. **Start Mobile App**:
   ```bash
   cd mobile
   flutter run -d web-server --web-port 8080
   ```

3. **Register Account**:
   - Open http://localhost:8080
   - Click "Register"
   - Enter email and password

4. **Set Up Profile**:
   - Enter age, gender, height, weight
   - Select activity level and goal
   - App calculates your daily calorie target

5. **Start Tracking**:
   - Log meals from the dashboard
   - View nutrition analytics
   - Generate weekly meal plans

---

## 🏗️ Project Structure

```
smart-nutrition-tracker/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── auth.py              # JWT authentication
│   ├── models.py            # Pydantic models
│   ├── database.py          # MongoDB connection
│   ├── requirements.txt     # Python dependencies
│   ├── docker-compose.yml   # MongoDB setup
│   └── .env                 # Environment variables
│
└── mobile/
    ├── lib/
    │   ├── main.dart                    # App entry point
    │   ├── theme/app_theme.dart         # Custom theme
    │   ├── screens/
    │   │   ├── login_screen.dart        # Login/Register
    │   │   ├── profile_setup_screen.dart
    │   │   ├── dashboard_screen.dart    # Main dashboard
    │   │   ├── meal_log_screen.dart     # Meal logging
    │   │   ├── meal_plan_screen.dart    # Meal planning
    │   │   └── settings_screen.dart     # Settings & logout
    │   └── services/api_service.dart    # Backend API calls
    └── pubspec.yaml            # Flutter dependencies
```

---

## 🔒 Security Features

- ✅ Argon2 password hashing (OWASP recommended)
- ✅ JWT tokens with 30-minute expiry
- ✅ Rate limiting on authentication endpoints
- ✅ Input validation (age, height, weight constraints)
- ✅ CORS protection
- ✅ Environment-based secrets

---

## 🛠️ Development

### Hot Reload (Backend)

The backend runs with `--reload` flag, so code changes are automatically applied.

### Hot Reload (Mobile)

While `flutter run` is active, press:
- `r` - Hot reload
- `R` - Hot restart
- `q` - Quit

---

## 📊 Tech Stack

**Backend:**
- FastAPI
- MongoDB
- Argon2-cffi
- python-jose (JWT)
- Loguru
- SlowAPI (rate limiting)

**Mobile:**
- Flutter
- fl_chart (charts)
- http (API calls)
- shared_preferences (storage)
- google_fonts

---

## 🐛 Troubleshooting

### Backend Issues

**MongoDB connection failed:**
```bash
docker-compose down
docker-compose up -d
```

**Port 8001 already in use:**
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9
```

### Mobile Issues

**Flutter web blank page:**
- Make sure backend is running on port 8001
- Check browser console for errors
- Try production build: `flutter build web --release`

**Android build failed:**
```bash
flutter doctor
flutter clean
flutter pub get
```

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Taher Awad**
- GitHub: [@Taher-awad](https://github.com/Taher-awad)

---

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- Flutter team for the cross-platform framework
- fl_chart for beautiful charts
- Cronometer & MyFitnessPal for UI inspiration
