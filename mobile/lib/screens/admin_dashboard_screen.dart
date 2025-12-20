import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AdminDashboardScreen extends StatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  Map<String, dynamic>? _stats;
  bool _isLoadingStats = false;
  
  // Food Management State
  final _foodNameController = TextEditingController();
  final _caloriesController = TextEditingController();
  final _proteinController = TextEditingController();
  final _carbsController = TextEditingController();
  final _fatsController = TextEditingController();
  bool _isAddingFood = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadStats();
  }

  @override
  void dispose() {
    _tabController.dispose();
    _foodNameController.dispose();
    _caloriesController.dispose();
    _proteinController.dispose();
    _carbsController.dispose();
    _fatsController.dispose();
    super.dispose();
  }

  Future<void> _loadStats() async {
    setState(() => _isLoadingStats = true);
    final stats = await ApiService.getSystemStats();
    if (mounted) {
      setState(() {
        _stats = stats;
        _isLoadingStats = false;
      });
    }
  }

  Future<void> _addFood() async {
    if (_foodNameController.text.isEmpty || _caloriesController.text.isEmpty) return;
    
    setState(() => _isAddingFood = true);
    final success = await ApiService.addGlobalFood({
      'name': _foodNameController.text,
      'calories': double.tryParse(_caloriesController.text) ?? 0,
      'protein': double.tryParse(_proteinController.text) ?? 0,
      'carbs': double.tryParse(_carbsController.text) ?? 0,
      'fats': double.tryParse(_fatsController.text) ?? 0,
      'is_custom': false
    });
    
    setState(() => _isAddingFood = false);
    
    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Food added successfully!')));
        _foodNameController.clear();
        _caloriesController.clear();
        _proteinController.clear();
        _carbsController.clear();
        _fatsController.clear();
        _loadStats(); // Update stats
      } else {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Failed to add food.')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Admin Dashboard'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(icon: Icon(Icons.analytics), text: 'Stats'),
            Tab(icon: Icon(Icons.restaurant_menu), text: 'Manage Foods'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildStatsTab(),
          _buildFoodManagementTab(),
        ],
      ),
    );
  }

  Widget _buildStatsTab() {
    if (_isLoadingStats) return const Center(child: CircularProgressIndicator());
    if (_stats == null) return const Center(child: Text('Failed to load stats. Are you an Admin?'));

    return RefreshIndicator(
      onRefresh: _loadStats,
      child: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          Row(
            children: [
              Expanded(child: _buildStatCard('Total Users', Icons.people, _stats!['total_users'].toString(), Colors.blue)),
              const SizedBox(width: 16),
              Expanded(child: _buildStatCard('Active (7d)', Icons.local_fire_department, _stats!['active_users_last_7_days'].toString(), Colors.redAccent)),
            ],
          ),
          _buildStatCard('Meals Logged', Icons.restaurant, _stats!['total_meals_logged'].toString(), Colors.green),
          _buildStatCard('Global Foods', Icons.list_alt, _stats!['total_food_items'].toString(), Colors.orange),
        ],
      ),
    );
  }

  Widget _buildStatCard(String title, IconData icon, String value, Color color) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: color.withOpacity(0.1), shape: BoxShape.circle),
              child: Icon(icon, color: color, size: 32),
            ),
            const SizedBox(width: 24),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: Theme.of(context).textTheme.titleMedium?.copyWith(color: Colors.grey[600])),
                Text(value, style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.bold)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFoodManagementTab() {
    return Column(
      children: [
        // Add Food Form
        ExpansionTile(
          title: const Text('Add New Global Food'),
          children: [
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                   TextField(controller: _foodNameController, decoration: const InputDecoration(labelText: 'Food Name', border: OutlineInputBorder())),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(child: TextField(controller: _caloriesController, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Calories', border: OutlineInputBorder()))),
                      const SizedBox(width: 8),
                      Expanded(child: TextField(controller: _proteinController, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Protein (g)', border: OutlineInputBorder()))),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(child: TextField(controller: _carbsController, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Carbs (g)', border: OutlineInputBorder()))),
                      const SizedBox(width: 8),
                      Expanded(child: TextField(controller: _fatsController, keyboardType: TextInputType.number, decoration: const InputDecoration(labelText: 'Fats (g)', border: OutlineInputBorder()))),
                    ],
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: _isAddingFood ? null : _addFood,
                      icon: _isAddingFood ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.add),
                      label: Text(_isAddingFood ? 'Adding...' : 'Add Food Item'),
                      style: ElevatedButton.styleFrom(padding: const EdgeInsets.all(16)),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        const Divider(height: 1),
        Expanded(child: _buildFoodList()),
      ],
    );
  }

  Widget _buildFoodList() {
    return FutureBuilder<List<dynamic>?>(
      future: ApiService.getGlobalFoods(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const Center(child: Text('No global foods found.'));
        }

        final foods = snapshot.data!;
        return ListView.builder(
          itemCount: foods.length,
          itemBuilder: (context, index) {
            final food = foods[index];
            return ListTile(
              title: Text(food['name']),
              subtitle: Text('${food['calories']} kcal | P: ${food['protein']}g C: ${food['carbs']}g F: ${food['fats']}g'),
              trailing: IconButton(
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () => _deleteFood(food['id'], food['name']),
              ),
            );
          },
        );
      },
    );
  }

  Future<void> _deleteFood(int id, String name) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Food'),
        content: Text('Delete "$name"? This might affect users.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          TextButton(onPressed: () => Navigator.pop(context, true), child: const Text('Delete', style: TextStyle(color: Colors.red))),
        ],
      ),
    );

    if (confirm == true) {
      final success = await ApiService.deleteFood(id);
      if (mounted) {
        if (success) {
          setState(() {}); // Rebuild to refresh FutureBuilder
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Food deleted.')));
           _loadStats();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Failed to delete (might be in use).')));
        }
      }
    }
  }
}
