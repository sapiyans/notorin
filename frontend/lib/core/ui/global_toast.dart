import 'package:another_flushbar/flushbar.dart';
import 'package:flutter/material.dart';

class GlobalToast {
  static final navigatorKey = GlobalKey<NavigatorState>();

  static BuildContext? get _context => navigatorKey.currentContext;

  static void _show({
    required String message,
    required Color bgColor,
    required Color textColor,
    required IconData icon,
  }) {
    final context = _context;
    if (context == null) return;

    Flushbar(
      messageText: Text(
        message,
        style: TextStyle(
          color: textColor,
          fontSize: 14,
          fontWeight: FontWeight.w500,
        ),
      ),

      icon: Container(
        padding: const EdgeInsets.all(6),
        decoration: BoxDecoration(
          color: textColor.withValues(alpha: 0.15),
          shape: BoxShape.circle,
        ),
        child: Icon(icon, color: textColor, size: 18),
      ),

      duration: const Duration(seconds: 3),
      flushbarPosition: FlushbarPosition.TOP,
      textDirection: Directionality.of(context),

      margin: const EdgeInsets.only(top: 20, right: 1),
      maxWidth: 380,
      borderRadius: BorderRadius.circular(12),

      backgroundColor: bgColor,

      animationDuration: const Duration(milliseconds: 250),

      boxShadows: [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.2),
          blurRadius: 20,
          offset: const Offset(0, 6),
        ),
      ],

      isDismissible: true,
      dismissDirection: FlushbarDismissDirection.HORIZONTAL,
    ).show(context);
  }

  static void error(String message) {
    final context = _context;
    if (context == null) return;

    final theme = Theme.of(context).colorScheme;

    _show(
      message: message,
      bgColor: theme.error,
      textColor: theme.onError,
      icon: Icons.close,
    );
  }

  static void success(String message) {
    final context = _context;
    if (context == null) return;

    final theme = Theme.of(context).colorScheme;

    _show(
      message: message,
      bgColor: theme.primary, // pode customizar depois
      textColor: theme.onPrimary,
      icon: Icons.check,
    );
  }

  static void warning(String message) {
    final context = _context;
    if (context == null) return;

    final theme = Theme.of(context).colorScheme;

    _show(
      message: message,
      bgColor: theme.secondary,
      textColor: theme.onSecondary,
      icon: Icons.warning_amber,
    );
  }

  static void info(String message) {
    final context = _context;
    if (context == null) return;

    final theme = Theme.of(context).colorScheme;

    _show(
      message: message,
      bgColor: theme.surface,
      textColor: theme.onSurface,
      icon: Icons.info_outline,
    );
  }
}