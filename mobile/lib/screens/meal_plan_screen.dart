import 'package:flutter/material.dart';
import '../services/api_service.dart';

class MealPlanScreen extends StatefulWidget {
  const MealPlanScreen({super.key});

  @override
  State<MealPlanScreen> createState() => _MealPlanScreenState();
}

class _MealPlanScreenState extends State<MealPlanScreen> {
  bool _isLoading = false;
  List<dynamic>? _variations;
  int _currentIndex = 0;
  final PageController _pageController = PageController(viewportFraction: 0.85);

  @override
  void initState() {
    super.initState();
    _loadVars();
  }

  Future<void> _loadVars() async {
    setState(() => _isLoading = true);
    final vars = await ApiService.getMealPlanVariations();
    if (mounted) {
      setState(() {
        _variations = vars;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Meal Plans')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _variations == null || _variations!.isEmpty
              ? _buildEmptyState()
              : Column(
                  children: [
                    const Padding(
                      padding: EdgeInsets.all(16.0),
                      child: Text(
                        "Swipe to choose your goal",
                        style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                    ),
                    SizedBox(
                      height: 400, // Carousel Height
                      child: PageView.builder(
                        controller: _pageController,
                        itemCount: _variations!.length,
                        onPageChanged: (index) => setState(() => _currentIndex = index),
                        itemBuilder: (context, index) {
                          return _buildPlanCard(_variations![index], index == _currentIndex);
                        },
                      ),
                    ),
                    const SizedBox(height: 20),
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16.0),
                        child: _buildDetailSection(_variations![_currentIndex]),
                      ),
                    ),
                  ],
                ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('No plans available.'),
          ElevatedButton(onPressed: _loadVars, child: const Text('Retry')),
        ],
      ),
    );
  }

  Widget _buildPlanCard(dynamic plan, bool isActive) {
    return AnimatedScale(
      scale: isActive ? 1.0 : 0.9,
      duration: const Duration(milliseconds: 300),
      child: Card(
        elevation: isActive ? 8 : 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 16),
        color: isActive ? Theme.of(context).primaryColor : Colors.grey[200],
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.restaurant_menu,
                size: 60,
                color: isActive ? Colors.white : Colors.grey[600],
              ),
              const SizedBox(height: 20),
              Text(
                plan['goal_name'],
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: isActive ? Colors.white : Colors.black87,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 12),
              Text(
                plan['description'],
                style: TextStyle(
                  fontSize: 16,
                  color: isActive ? Colors.white70 : Colors.grey[700],
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDetailSection(dynamic plan) {
    return DefaultTabController(
      length: 2,
      child: Column(
        children: [
          const TabBar(
            labelColor: Colors.blue,
            unselectedLabelColor: Colors.grey,
            tabs: [
              Tab(text: "Sample Meals"),
              Tab(text: "Grocery List"),
            ],
          ),
          Expanded(
            child: TabBarView(
              children: [
                _buildMealsList(plan['meals']),
                _buildGroceryList(plan['grocery_list']),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMealsList(List<dynamic> meals) {
    // Group by Day? Or just simple list
    // ApiService logic returns flattened list. Let's just show nicely.
    return ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: meals.length,
      itemBuilder: (context, index) {
         final m = meals[index];
         return ListTile(
           leading: const Icon(Icons.timer_outlined),
           title: Text("${m['meal_type'].toString().toUpperCase()} - ${m['food']['name']}"),
           subtitle: Text("Day ${DateTime.parse(m['date']).day}"),
         );
      },
    );
  }

  Widget _buildGroceryList(List<dynamic>? groceryList) {
    if (groceryList == null || groceryList.isEmpty) {
      return const Center(child: Text("Empty list"));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(8),
      itemCount: groceryList.length,
      itemBuilder: (context, index) {
        return CheckboxListTile(
          value: false, 
          onChanged: (val) {}, // Stateless for now
          title: Text(groceryList[index].toString()),
        );
      },
    );
  }
}
