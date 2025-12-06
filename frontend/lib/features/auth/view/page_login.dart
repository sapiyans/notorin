import 'package:flutter/material.dart';
import 'package:frontend/features/auth/view/controller_form.dart';
import 'package:smooth_corner/smooth_corner.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      backgroundColor: theme.scaffoldBackgroundColor,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 550),
            child: SmoothCard(
              smoothness: 0.8,
              borderRadius: BorderRadius.circular(45),
              color: theme.cardColor,
              child: const Padding(
                padding: EdgeInsets.all(35),
                child: ControllerForm(),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
