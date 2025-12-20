import 'package:flutter/material.dart';
import '../services/api_service.dart';

class MealLogScreen extends StatefulWidget {
  const MealLogScreen({super.key});

  @override
  State<MealLogScreen> createState() => _MealLogScreenState();
}

class _MealLogScreenState extends State<MealLogScreen> {
  final _searchController = TextEditingController();
  List<dynamic> _foods = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _searchFoods();
  }

  Future<void> _searchFoods([String query = '']) async {
    setState(() => _isLoading = true);
    final foods = await ApiService.searchFoods(query);
    setState(() {
      _foods = foods ?? [];
      _isLoading = false;
    });
  }

  Future<void> _logFood(Map<String, dynamic> food) async {
    final success = await ApiService.logMeal(food, "snack"); // Defaulting to snack for demo
    if (success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Meal Logged!')));
      Navigator.pop(context);
    }
  }

  Future<void> _scanMeal() async {
    // Mock AI Scan
    setState(() => _isLoading = true);
    final food = await ApiService.recognizeImage();
    setState(() => _isLoading = false);
    
    if (food != null && mounted) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('AI Recognized Food'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Name: ${food['name']}'),
              Text('Calories: ${food['calories']}'),
              Text('Protein: ${food['protein']}g'),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
                _logFood(food);
              },
              child: const Text('Log This'),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Log Meal')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    decoration: const InputDecoration(
                      labelText: 'Search Food',
                      prefixIcon: Icon(Icons.search),
                    ),
                    onSubmitted: _searchFoods,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.camera_alt),
                  onPressed: _scanMeal,
                  tooltip: 'AI Scan',
                ),
              ],
            ),
          ),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: _foods.length,
                    itemBuilder: (context, index) {
                      final food = _foods[index];
                      return ListTile(
                        title: Text(food['name']),
                        subtitle: Text('${food['calories']} kcal | P: ${food['protein']}g'),
                        trailing: IconButton(
                          icon: const Icon(Icons.add_circle_outline),
                          onPressed: () => _logFood(food),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
