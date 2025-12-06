import 'package:flutter/material.dart';
import 'package:frontend/core/responsive/app_container.dart';
import 'package:go_router/go_router.dart';

class Header extends StatelessWidget implements PreferredSizeWidget {
  final VoidCallback? onMenuPressed;

  const Header({super.key, this.onMenuPressed});

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;

    return AppBar(
      actions: [
        IconButton(
          icon: Icon(Icons.menu, color: cs.onInverseSurface),
          onPressed: onMenuPressed,
        ),
      ],
      title: AppContainer(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            InkWell(
              onTap: () => context.goNamed('dashboard'),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [cs.primary, cs.tertiary],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Icon(Icons.note, color: cs.onPrimary, size: 24),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Notorin',
                    style: TextStyle(
                      color: cs.onInverseSurface,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
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

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
