import 'package:flutter/material.dart';
import 'package:frontend/core/config/app_config.dart';
import 'package:frontend/features/auth/services/login.dart';
import 'package:go_router/go_router.dart';
import 'custom_drawer.dart';
import 'header.dart';

class ScaffoldWithDrawer extends StatefulWidget {
  final Widget child;
  final int selectedIndex;
  final DrawerSide drawerSide;

  const ScaffoldWithDrawer({
    super.key,
    required this.child,
    required this.selectedIndex,
    this.drawerSide = DrawerSide.right,
  });

  @override
  State<ScaffoldWithDrawer> createState() => _ScaffoldWithDrawerState();
}

class _ScaffoldWithDrawerState extends State<ScaffoldWithDrawer> {
  final CustomDrawerController _drawerController = CustomDrawerController();

  void _closeAndNavigate(VoidCallback action) {
    _drawerController.close();
    action();
  }

  Future<void> _logout() async {
    await UserLoginService().logout();
    if (mounted) context.go('/login');
  }

  Widget _buildDrawerHeader(ColorScheme cs) {
    final isHorizontal = widget.drawerSide == DrawerSide.left ||
        widget.drawerSide == DrawerSide.right;

    if (isHorizontal) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.fromLTRB(20, 48, 20, 20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [cs.primary, cs.primaryContainer],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(Icons.note, color: cs.onPrimary, size: 40),
            const SizedBox(height: 12),
            Text(
              AppConfig.appName,
              style: TextStyle(
                color: cs.onPrimary,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              AppConfig.appDescription,
              style: TextStyle(color: cs.onPrimary.withValues(alpha: 0.7), fontSize: 14),
            ),
          ],
        ),
      );
    }

    return Container(
      height: double.infinity,
      width: 120,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [cs.primary, cs.primaryContainer],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.note, color: cs.onPrimary, size: 40),
          const SizedBox(height: 8),
          Text(
            AppConfig.appName,
            style: TextStyle(
              color: cs.onPrimary,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDrawerContent(ColorScheme cs) {
    final isHorizontal = widget.drawerSide == DrawerSide.left ||
        widget.drawerSide == DrawerSide.right;

    return Container(
      color: cs.surface,
      child: isHorizontal
          ? Column(
              children: [
                _buildDrawerHeader(cs),
                _buildMenuItem(
                  icon: Icons.home_outlined,
                  label: 'Início',
                  color: cs.onSurface,
                  onTap: () => _closeAndNavigate(() => context.goNamed('dashboard')),
                ),
                const Spacer(),
                _buildMenuItem(
                  icon: Icons.logout,
                  label: 'Sair',
                  color: cs.error,
                  onTap: () => _closeAndNavigate(_logout),
                ),
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(
                    'Versão ${AppConfig.appVersion}',
                    style: TextStyle(fontSize: 12, color: cs.onSurfaceVariant),
                  ),
                ),
              ],
            )
          : Row(
              children: [
                _buildDrawerHeader(cs),
                Expanded(
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        _buildMenuItemHorizontal(
                          icon: Icons.home_outlined,
                          label: 'Início',
                          color: cs.onSurface,
                          onTap: () => _closeAndNavigate(() => context.goNamed('dashboard')),
                        ),
                        _buildMenuItemHorizontal(
                          icon: Icons.logout,
                          label: 'Sair',
                          color: cs.error,
                          onTap: () => _closeAndNavigate(_logout),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    required Color color,
  }) {
    return ListTile(
      leading: Icon(icon, color: color),
      title: Text(label, style: TextStyle(color: color)),
      onTap: onTap,
    );
  }

  Widget _buildMenuItemHorizontal({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    required Color color,
  }) {
    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 24, color: color),
            const SizedBox(height: 4),
            Text(label, style: TextStyle(fontSize: 12, color: color)),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    final drawerSize = (widget.drawerSide == DrawerSide.left ||
            widget.drawerSide == DrawerSide.right)
        ? 280.0
        : 120.0;

    return CustomDrawer(
      side: widget.drawerSide,
      controller: _drawerController,
      drawerContent: _buildDrawerContent(cs),
      size: drawerSize,
      maxBlurIntensity: 5,
      maxOverlayOpacity: 0.6,
      showDragHandle: true,
      dragHandleColor: cs.outlineVariant,
      animationDuration: const Duration(milliseconds: 300),
      animationCurve: Curves.easeOutCubic,
      child: Scaffold(
        appBar: Header(onMenuPressed: _drawerController.toggle),
        body: widget.child,
      ),
    );
  }
}
