import 'package:flutter/material.dart';

class AppConfig {
  static const String appName = 'Notorin';
  static const String appVersion = '1.0.0';
  static const String appDescription = 'Organize suas notas';
  static const String apiBaseUrl = 'https://api.notorin.com/api/v1';

  // Roxo
  static const Color primary = Color(0xFF6C63FF);
  static const Color primaryLight = Color(0xFF918AFF);
  static const Color primaryDark = Color(0xFF4A42D8);
  
  // Cores de feedback
  static const Color error = Color(0xFFE53935);
  static const Color success = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFFA726);
  
  // Tema Claro
  static const Color lightBackground = Color.fromARGB(255, 234, 234, 240);
  static const Color lightSurface = Color.fromARGB(255, 243, 243, 253);
  
  // Tema Escuro
  static const Color darkBackground = Color(0xFF1A1A2E);
  static const Color darkSurface = Color(0xFF1E1E38);
  static const Color darkCard = Color(0xFF2A2A45);
}