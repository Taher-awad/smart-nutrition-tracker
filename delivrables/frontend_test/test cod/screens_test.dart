import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/main.dart';
import 'package:mobile/screens/login_screen.dart';
import 'package:mobile/screens/dashboard_screen.dart';
import 'package:mobile/screens/meal_log_screen.dart';
import 'package:mobile/services/api_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('Smart Nutrition Tracker Widget Tests', () {
    
    testWidgets('TC001: Login Screen displays correctly', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Verify Login UI Elements
      expect(find.text('Smart Nutrition Tracker'), findsOneWidget);
      expect(find.widgetWithText(TextField, 'Email'), findsOneWidget);
      expect(find.widgetWithText(TextField, 'Password'), findsOneWidget);
      expect(find.text('Login'), findsOneWidget);
      expect(find.text('Register'), findsOneWidget);
    });

    testWidgets('TC002: Login Screen allows text input', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Enter text in fields
      await tester.enterText(find.widgetWithText(TextField, 'Email'), 'user@example.com');
      await tester.enterText(find.widgetWithText(TextField, 'Password'), 'securepass');
      
      // Verify text was entered
      expect(find.text('user@example.com'), findsOneWidget);
    });

    testWidgets('TC003: Dashboard Screen structure', (WidgetTester tester) async {
      // Pump Dashboard directly (isolated test)
      await tester.pumpWidget(const MaterialApp(
        home: DashboardScreen(),
      ));
      
      // Pump once to build
      await tester.pump();
      
      // Verify AppBar title
      expect(find.text('My Nutrition Dashboard'), findsOneWidget);
    });

    testWidgets('TC004: Meal Log Screen structure', (WidgetTester tester) async {
      // Pump MealLogScreen directly
      await tester.pumpWidget(const MaterialApp(
        home: MealLogScreen(),
      ));
      await tester.pump();
      
      // Verify Search field exists
      expect(find.text('Search Food'), findsOneWidget);
    });

    testWidgets('TC005: Login button is tappable', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Find and tap login button
      final loginButton = find.text('Login');
      expect(loginButton, findsOneWidget);
      
      // Verify button responds to tap (no crash)
      await tester.tap(loginButton);
      await tester.pump();
      
      // Test passes if no exception is thrown
    });

    testWidgets('TC006: Register button is tappable', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Find and tap register button
      final registerButton = find.text('Register');
      expect(registerButton, findsOneWidget);
      
      await tester.tap(registerButton);
      await tester.pump();
      
      // Test passes if no exception is thrown
    });
  });
}
