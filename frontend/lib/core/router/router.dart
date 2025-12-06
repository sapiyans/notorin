import 'package:frontend/core/ui/global_toast.dart';
import 'package:frontend/features/auth/services/login.dart';
import 'package:frontend/features/auth/view/page_login.dart';
import 'package:frontend/features/home/page_home.dart';
import 'package:go_router/go_router.dart';

final router = GoRouter(
  initialLocation: '/login',
  navigatorKey: GlobalToast.navigatorKey,
  redirect: (context, state) async {
    final isLoggedIn = await UserLoginService().isLoggedIn();
    final isOnLogin = state.matchedLocation == '/login';

    if (!isLoggedIn && !isOnLogin) return '/login';
    if (isLoggedIn && isOnLogin) return '/dashboard';
    return null;
  },
  routes: [
    GoRoute(
      name: 'dashboard',
      path: '/dashboard',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      name: 'login',
      path: '/login',
      builder: (context, state) => const LoginPage(),
    ),
  ],
);
