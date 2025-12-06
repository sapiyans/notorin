import 'package:flutter/material.dart';
import 'package:frontend/features/auth/view/login_form.dart';
import 'package:frontend/features/auth/view/register_form.dart';
import 'package:frontend/shared/widgets/custom_card.dart';

enum AuthMode { login, register }

class ControllerForm extends StatefulWidget {
  const ControllerForm({super.key});

  @override
  State<ControllerForm> createState() => _StateControllerForm();
}

class _StateControllerForm extends State<ControllerForm> {
  AuthMode _mode = AuthMode.login;

  void _toggleForm() {
    setState(() {
      _mode = _mode == AuthMode.login ? AuthMode.register : AuthMode.login;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      spacing: 10,
      children: [
        CustomCard(
          child: _mode == AuthMode.register
              ? const RegisterForm()
              : const LoginForm(),
        ),
        TextButton(
          onPressed: _toggleForm,
          child: Text(
            _mode == AuthMode.register ? 'Ir para Login' : 'Ir para Registro',
          ),
        ),
      ],
    );
  }
}
