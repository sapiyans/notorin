// home.dart
import 'package:flutter/material.dart';
import 'package:frontend/shared/widgets/custom_card.dart';
import 'package:frontend/shared/widgets/layout/scaffold_with_drawer.dart';
import 'package:frontend/shared/widgets/layout/custom_drawer.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  // Controllers para os drawers
  final CustomDrawerController _leftDrawerController = CustomDrawerController();
  final CustomDrawerController _rightDrawerController = CustomDrawerController();
  final CustomDrawerController _bottomDrawerController = CustomDrawerController();
  final CustomDrawerController _topDrawerController = CustomDrawerController();

  @override
  void initState() {
    super.initState();
  }

  // Conteúdo padrão para TODOS os drawers (simples, apenas ícones e textos)
  Widget buildDrawerContent(String title, IconData icon, Color color) {
    final cs = Theme.of(context).colorScheme;
    return Container(
      color: cs.surface,
      child: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [color, color],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(icon, color: Colors.white, size: 40),
                const SizedBox(height: 12),
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Text(
                  'Menu com scroll vertical',
                  style: TextStyle(color: Colors.white70),
                ),
              ],
            ),
          ),
          // Lista com scroll vertical
          Expanded(
            child: ListView.builder(
              itemCount: 30,
              itemBuilder: (context, index) {
                return ListTile(
                  leading: Icon(
                    Icons.menu,
                    color: color,
                  ),
                  title: Text('Item ${index + 1}'),
                  subtitle: Text('Descrição simples do item ${index + 1}'),
                  trailing: Icon(Icons.chevron_right, color: color),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Scaffold principal
        ScaffoldWithDrawer(
          selectedIndex: 0,
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Bem-vindo ao Notorin!',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    'Teste de Scroll nos Drawers',
                    style: TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                  const SizedBox(height: 40),
                  
                  // Botão Drawer Top
                  ElevatedButton.icon(
                    onPressed: () => _topDrawerController.open(),
                    icon: const Icon(Icons.arrow_downward),
                    label: const Text('Abrir Drawer Top (Scroll Vertical)'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.pink,
                      foregroundColor: Colors.white,
                      minimumSize: const Size(300, 60),
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  // Botão Drawer Esquerdo
                  ElevatedButton.icon(
                    onPressed: () => _leftDrawerController.open(),
                    icon: const Icon(Icons.arrow_back),
                    label: const Text('Abrir Drawer Esquerdo (Scroll Vertical)'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                      foregroundColor: Colors.white,
                      minimumSize: const Size(300, 60),
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  // Botão Drawer Direito
                  ElevatedButton.icon(
                    onPressed: () => _rightDrawerController.open(),
                    icon: const Icon(Icons.arrow_forward),
                    label: const Text('Abrir Drawer Direito (Scroll Vertical)'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                      minimumSize: const Size(300, 60),
                    ),
                  ),
                  const SizedBox(height: 20),
                  
                  // Botão Drawer Bottom
                  ElevatedButton.icon(
                    onPressed: () => _bottomDrawerController.open(),
                    icon: const Icon(Icons.arrow_upward),
                    label: const Text('Abrir Drawer Bottom (Scroll Vertical)'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orange,
                      foregroundColor: Colors.white,
                      minimumSize: const Size(300, 60),
                    ),
                  ),
                  
                  const SizedBox(height: 40),
                  
                  // Card informativo
                  CustomCard(
                    child: const Column(
                      children: [
                        Text(
                          '🧪 Teste de Conflito Scroll vs Drawer',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Abra qualquer drawer e tente scrollar dentro dele',
                          style: TextStyle(fontSize: 12),
                          textAlign: TextAlign.center,
                        ),
                        SizedBox(height: 4),
                        Text(
                          'O scroll DEVE funcionar sem fechar o drawer',
                          style: TextStyle(fontSize: 12, color: Colors.green),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        
        // Drawer Top
        CustomDrawer(
          side: DrawerSide.top,
          controller: _topDrawerController,
          drawerContent: buildDrawerContent('Drawer Top', Icons.arrow_downward, Colors.pink),
          size: 350,
          maxBlurIntensity: 8,
          maxOverlayOpacity: 0.7,
          showDragHandle: true,
          animationDuration: const Duration(milliseconds: 300),
        ),
        
        // Drawer Esquerdo
        CustomDrawer(
          side: DrawerSide.left,
          controller: _leftDrawerController,
          drawerContent: buildDrawerContent('Drawer Esquerdo', Icons.arrow_back, Colors.blue),
          size: 320,
          maxBlurIntensity: 5,
          maxOverlayOpacity: 0.6,
          showDragHandle: true,
          animationDuration: const Duration(milliseconds: 300),
        ),
        
        // Drawer Direito
        CustomDrawer(
          side: DrawerSide.right,
          controller: _rightDrawerController,
          drawerContent: buildDrawerContent('Drawer Direito', Icons.arrow_forward, Colors.green),
          size: 1200,
          maxBlurIntensity: 5,
          maxOverlayOpacity: 0.6,
          showDragHandle: true,
          
          animationDuration: const Duration(milliseconds: 300),
        ),
        
        // Drawer Bottom
        CustomDrawer(
          side: DrawerSide.bottom,
          controller: _bottomDrawerController,
          drawerContent: buildDrawerContent('Drawer Bottom', Icons.arrow_upward, Colors.orange),
          size: 280,
          showDragHandle: true,
          animationDuration: const Duration(milliseconds: 300),
        ),
      ],
    );
  }
}