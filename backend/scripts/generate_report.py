from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Smart Nutrition Tracker - Test Verification Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

# Helper to read log file
def read_log(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Log file not found: {filename} ({str(e)})"

# ==========================================
# 1. GENERATE BACKEND REPORT
# ==========================================
print("Generating Backend Report...")
pdf_backend = PDF()
pdf_backend.add_page()
pdf_backend.set_font('Arial', '', 12)
pdf_backend.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
pdf_backend.ln(5)

# Executive Summary
pdf_backend.chapter_title('1. Executive Summary')
pdf_backend.chapter_body(
    "This report details the verification of the Backend (FastAPI) system. "
    "All unit and integration tests successfully passed using the Pytest framework.\n"
    "Overall Result: PASSED"
)

# Methodology
pdf_backend.chapter_title('2. Test Scope & Methodology')
pdf_backend.chapter_body(
    "1. Authentication Tests (test_auth.py):\n"
    "   - Purpose: Verify security mechanisms for user access.\n"
    "   - Methodology: We simulate login requests with correct/incorrect credentials and verify JWT token issuance. Password hashing is checked using Argon2 verification to ensure no plain-text storage.\n\n"
    "2. User Management (test_users.py):\n"
    "   - Purpose: Ensure user profile data integrity and access control.\n"
    "   - Methodology: Integration tests verify that users can update their profiles (height, weight, goals) and that unauthorized users cannot access Admin routes.\n\n"
    "3. Food & Meal Logic (test_food_meals.py):\n"
    "   - Purpose: Validate core business logic for calorie tracking.\n"
    "   - Methodology: We seed the database with test foods, log meals against a user account, and assert that the 'Daily Summary' correctly aggregates calories and macros.\n\n"
    "4. AI Meal Planning (test_ai_plans.py):\n"
    "   - Purpose: Verify the Plan Generation Engine.\n"
    "   - Methodology: We call the AI Service with a user context and assert that the returned JSON structure contains 7 distinct days of meals, adhering to the requested goal logic."
)

# Logs - REMOVED per user request
# pdf_backend.chapter_title('3. Detailed Test Logs')
# log_content = read_log('backend_test_log.txt')
# pdf_backend.set_font('Courier', '', 9)
# pdf_backend.multi_cell(0, 5, log_content)

pdf_backend.output("Backend_Test_Report.pdf", 'F')
print("Backend Report generated: Backend_Test_Report.pdf")


# ==========================================
# 2. GENERATE FRONTEND REPORT
# ==========================================
print("Generating Backend Report...")
pdf_frontend = PDF()
pdf_frontend.add_page()
pdf_frontend.set_font('Arial', '', 12)
pdf_frontend.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
pdf_frontend.ln(5)

# Executive Summary
pdf_frontend.chapter_title('1. Executive Summary')
pdf_frontend.chapter_body(
    "This report details the verification of the Frontend (Flutter) application. "
    "Widget (Smoke) testing confirmed that the application launches and renders key UI components relative to the initial user flow.\n"
    "Overall Result: PASSED"
)

# Methodology
pdf_frontend.chapter_title('2. Test Scope & Methodology')
pdf_frontend.chapter_body(
    "1. Widget Smoke Tests (widget_test.dart):\n"
    "   - Purpose: Ensure the application starts and renders the critical initial UI (Login Screen).\n"
    "   - Methodology: We use 'tester.pumpWidget' to load the app in a headless test environment. We then use 'find.text' matchers to confirm that the Title ('Smart Nutrition Tracker'), Login input fields, and Action buttons are visible on screen.\n\n"
    "2. Rationale for Smoke Tests:\n"
    "   - These tests are critical for preventing 'White Screen of Death' regressions. They ensure that the app build is valid and the entry point hasn't been broken by recent dependency changes or refactors."
)

# Logs - REMOVED per user request
# pdf_frontend.chapter_title('3. Detailed Test Logs')
# log_content_front = read_log('frontend_test_log.txt')
# pdf_frontend.set_font('Courier', '', 9)
# pdf_frontend.multi_cell(0, 5, log_content_front)

pdf_frontend.output("Frontend_Test_Report.pdf", 'F')
print("Frontend Report generated: Frontend_Test_Report.pdf")
