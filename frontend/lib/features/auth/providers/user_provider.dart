import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/features/auth/services/login.dart';

final userServiceProvider = Provider<UserLoginService>((ref) {
  return UserLoginService();
});
