import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../services/api_service.dart';
import 'meal_log_screen.dart';
import 'meal_plan_screen.dart';
import 'settings_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? _analytics;
  bool _isLoading = true;
  int _waterGlasses = 0;

  @override
  void initState() {
    super.initState();
    _loadAnalytics();
  }

  Future<void> _loadAnalytics() async {
    print('Refreshing Analytics Data...'); // Debug print
    final data = await ApiService.getAnalytics();
    if (mounted) {
      setState(() {
        _analytics = data;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Nutrition Dashboard'), // Updated title to verify change
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Today's Section
                  Text(
                    '📊 Today',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  const SizedBox(height: 16),
                  _buildCalorieProgress(),
                  const SizedBox(height: 16),
                  _buildMacroDistribution(),
                  const SizedBox(height: 16),
                  _buildNutrientDetails(),
                  const SizedBox(height: 16),
                  _buildWaterTracker(),
                  const SizedBox(height: 32),
                  
                  // Weekly Section
                  Text(
                    '📈 Weekly Trends',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  const SizedBox(height: 16),
                  _buildWeeklyTrendChart(),
                  const SizedBox(height: 32),
                  
                  _buildActionButtons(context),
                ],
              ),
            ),
    );
  }

  Widget _buildCalorieProgress() {
    if (_analytics == null) return const SizedBox();
    final today = _analytics!['today'];
    final goal = _analytics!['goal'];
    final consumed = today['calories'];
    final remaining = (goal - consumed).clamp(0, goal);
    final percentage = (consumed / goal * 100).clamp(0, 100);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Today\'s Calories',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Text(
                  '${percentage.toInt()}%',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: Colors.green,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              child: Stack(
                children: [
                  PieChart(
                    PieChartData(
                      sections: [
                        PieChartSectionData(
                          value: consumed.toDouble(),
                          color: Colors.green,
                          radius: 60,
                          showTitle: false,
                        ),
                        PieChartSectionData(
                          value: remaining.toDouble(),
                          color: Colors.grey[300],
                          radius: 60,
                          showTitle: false,
                        ),
                      ],
                      sectionsSpace: 0,
                      centerSpaceRadius: 50,
                    ),
                  ),
                  Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          '${consumed.toInt()}',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 32,
                          ),
                        ),
                        const Text('consumed'),
                        Text(
                          'of ${goal.toInt()} kcal',
                          style: const TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildWeeklyTrendChart() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Weekly Calorie Trend',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(show: true, drawVerticalLine: false),
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        interval: 1,
                        getTitlesWidget: (value, meta) {
                          const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
                          final index = value.toInt();
                          if (index >= 0 && index < days.length) {
                            return Padding(
                              padding: const EdgeInsets.only(top: 8.0),
                              child: Text(
                                days[index],
                                style: const TextStyle(fontSize: 12),
                              ),
                            );
                          }
                          return const SizedBox();
                        },
                        reservedSize: 40,
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 50,
                        getTitlesWidget: (value, meta) {
                          return Text('${value.toInt()}', style: const TextStyle(fontSize: 10));
                        },
                      ),
                    ),
                    topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  borderData: FlBorderData(show: false),
                  lineBarsData: [
                    LineChartBarData(
                      spots: const [
                        FlSpot(0, 1800),
                        FlSpot(1, 2100),
                        FlSpot(2, 1950),
                        FlSpot(3, 2200),
                        FlSpot(4, 1900),
                        FlSpot(5, 2000),
                        FlSpot(6, 1850),
                      ],
                      isCurved: true,
                      color: Colors.green,
                      dotData: const FlDotData(show: true),
                      belowBarData: BarAreaData(
                        show: true,
                        color: Colors.green.withOpacity(0.3),
                      ),
                    ),
                  ],
                  minY: 1500,
                  maxY: 2500,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMacroDistribution() {
    if (_analytics == null) return const SizedBox();
    final today = _analytics!['today'];
    final protein = today['protein'].toDouble();
    final carbs = today['carbs'].toDouble();
    final fats = today['fats'].toDouble();
    final total = protein + carbs + fats;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Macronutrient Distribution',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: SizedBox(
                    height: 150,
                    child: total > 0
                        ? PieChart(
                            PieChartData(
                              sections: [
                                PieChartSectionData(
                                  value: protein,
                                  color: Colors.blue,
                                  title: '${(protein / total * 100).toInt()}%',
                                  radius: 50,
                                ),
                                PieChartSectionData(
                                  value: carbs,
                                  color: Colors.orange,
                                  title: '${(carbs / total * 100).toInt()}%',
                                  radius: 50,
                                ),
                                PieChartSectionData(
                                  value: fats,
                                  color: Colors.red,
                                  title: '${(fats / total * 100).toInt()}%',
                                  radius: 50,
                                ),
                              ],
                            ),
                          )
                        : const Center(child: Text('No data yet')),
                  ),
                ),
                const SizedBox(width: 20),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildLegendItem(Colors.blue, 'Protein', '${protein.toInt()}g'),
                    const SizedBox(height: 8),
                    _buildLegendItem(Colors.orange, 'Carbs', '${carbs.toInt()}g'),
                    const SizedBox(height: 8),
                    _buildLegendItem(Colors.red, 'Fats', '${fats.toInt()}g'),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLegendItem(Color color, String label, String value) {
    return Row(
      children: [
        Container(
          width: 16,
          height: 16,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 8),
        Text('$label: '),
        Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildNutrientDetails() {
    if (_analytics == null) return const SizedBox();
    final today = _analytics!['today'];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Today\'s Nutrition',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            _buildNutrientRow('Protein', today['protein'], Colors.blue),
            _buildNutrientRow('Carbs', today['carbs'], Colors.orange),
            _buildNutrientRow('Fats', today['fats'], Colors.red),
          ],
        ),
      ),
    );
  }

  Widget _buildNutrientRow(String name, num value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          SizedBox(
            width: 80,
            child: Text(name, style: const TextStyle(fontWeight: FontWeight.w500)),
          ),
          Expanded(
            child: LinearProgressIndicator(
              value: (value / 200).clamp(0.0, 1.0),
              backgroundColor: Colors.grey[300],
              color: color,
              minHeight: 8,
            ),
          ),
          const SizedBox(width: 12),
          SizedBox(
            width: 50,
            child: Text(
              '${value.toInt()}g',
              style: const TextStyle(fontWeight: FontWeight.bold),
              textAlign: TextAlign.right,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWaterTracker() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Water Intake', style: Theme.of(context).textTheme.titleLarge),
                Text(
                  '${(_waterGlasses * 250)}ml',
                  style: const TextStyle(color: Colors.blue, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  icon: const Icon(Icons.remove_circle_outline),
                  iconSize: 32,
                  color: Colors.red,
                  onPressed: () => setState(() => _waterGlasses = (_waterGlasses - 1).clamp(0, 20)),
                ),
                const SizedBox(width: 20),
                Column(
                  children: [
                    const Icon(Icons.water_drop, size: 48, color: Colors.blue),
                    Text(
                      '$_waterGlasses glasses',
                      style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(width: 20),
                IconButton(
                  icon: const Icon(Icons.add_circle_outline),
                  iconSize: 32,
                  color: Colors.green,
                  onPressed: () => setState(() => _waterGlasses++),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButtons(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        Expanded(
          child: ElevatedButton.icon(
            icon: const Icon(Icons.restaurant),
            label: const Text('Log Meal'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const MealLogScreen()),
              ).then((_) => _loadAnalytics());
            },
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: ElevatedButton.icon(
            icon: const Icon(Icons.calendar_month),
            label: const Text('Meal Plan'),
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(vertical: 16),
            ),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const MealPlanScreen()),
              ).then((_) => _loadAnalytics());
            },
          ),
        ),
      ],
    );
  }
}

