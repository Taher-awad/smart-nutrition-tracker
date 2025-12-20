import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService {
  // Use relative path in production (Nginx proxy), absolute localhost in dev
  static const String baseUrl = kReleaseMode ? '/api' : 'http://127.0.0.1:8001';

  static Future<String> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/token'),
        body: {
          'username': email,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['access_token'];
      } else if (response.statusCode == 401) {
        throw Exception('Invalid email or password');
      } else {
        throw Exception('Login failed: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Connection error: $e');
    }
  }

  static Future<String?> register(String email, String password, String fullName) async {
    final requestBody = {
      'email': email,
      'password': password,
      'full_name': fullName,
    };
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/users/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        return null; // Success
      } else {
        // Try to parse error message
        try {
          final errorData = jsonDecode(response.body);
          if (errorData['detail'] != null) {
            return errorData['detail'].toString();
          }
        } catch (_) {}
        return 'Registration failed: ${response.statusCode}';
      }
    } catch (e) {
      return 'Connection error: $e';
    }
  }

  static String? _token;

  static void setToken(String? token) {
    _token = token;
  } 
  
  static Future<Map<String, dynamic>?> getCurrentUser() async {
    if (_token == null) return null;
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/users/me/'),
        headers: {'Authorization': 'Bearer $_token'},
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      print('Error getting current user: $e');
    }
    return null;
  } 
  
  static Future<bool> updateProfile({
    required int age,
    required String gender,
    required double height,
    required double weight,
    required String activityLevel,
    required String goal,
  }) async {
    if (_token == null) return false;
    final response = await http.put(
      Uri.parse('$baseUrl/users/profile'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $_token',
      },
      body: jsonEncode({
        'age': age,
        'gender': gender,
        'height': height,
        'weight': weight,
        'activity_level': activityLevel,
        'goal': goal,
      }),
    );
    return response.statusCode == 200;
  }

  static Future<Map<String, dynamic>?> getAnalytics() async {
    if (_token == null) return null;
    final response = await http.get(
      Uri.parse('$baseUrl/analytics/summary'),
      headers: {'Authorization': 'Bearer $_token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  static Future<List<dynamic>?> searchFoods(String query) async {
    if (_token == null) return null;
    final response = await http.get(
      Uri.parse('$baseUrl/foods?search=$query'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  static Future<bool> logMeal(Map<String, dynamic> food, String mealType) async {
    if (_token == null) return false;
    final response = await http.post(
      Uri.parse('$baseUrl/meals'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $_token',
      },
      body: jsonEncode({
        'user_id': 'ignored', // Backend handles this
        'food_item': food,
        'date': DateTime.now().toIso8601String(),
        'meal_type': mealType,
      }),
    );
    return response.statusCode == 200;
  }

  static Future<Map<String, dynamic>?> recognizeImage() async {
    if (_token == null) return null;
    // Mock image upload - in real app, send multipart request
    final response = await http.post(
      Uri.parse('$baseUrl/ai/recognize'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  static Future<Map<String, dynamic>?> generateMealPlan() async {
    if (_token == null) return null;
    final response = await http.post(
      Uri.parse('$baseUrl/plans/generate'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  // --- Admin Endpoints ---

  static Future<Map<String, dynamic>?> getSystemStats() async {
    if (_token == null) return null;
    final response = await http.get(
      Uri.parse('$baseUrl/admin/stats'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  static Future<bool> addGlobalFood(Map<String, dynamic> foodData) async {
    if (_token == null) return false;
    final response = await http.post(
      Uri.parse('$baseUrl/admin/foods'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $_token',
      },
      body: jsonEncode(foodData),
    );
    return response.statusCode == 200;
  }

  static Future<bool> deleteFood(int foodId) async {
    if (_token == null) return false;
    final response = await http.delete(
      Uri.parse('$baseUrl/admin/foods/$foodId'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    return response.statusCode == 200;
  }
  static Future<List<dynamic>?> getGlobalFoods() async {
    if (_token == null) return null;
    final response = await http.get(
      Uri.parse('$baseUrl/admin/foods'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  static Future<List<dynamic>?> getMealPlanVariations() async {
    if (_token == null) return null;
    final response = await http.post(
      Uri.parse('$baseUrl/plans/variations'),
      headers: {'Authorization': 'Bearer $_token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }
}
