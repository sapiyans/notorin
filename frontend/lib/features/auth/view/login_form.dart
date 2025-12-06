import 'package:flutter/material.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/features/auth/providers/user_provider.dart';
import 'package:frontend/features/auth/models/register.dart';
import 'package:frontend/shared/widgets/layout/logo.dart';
import 'package:go_router/go_router.dart';

class LoginForm extends ConsumerStatefulWidget {
  const LoginForm({super.key});

  @override
  ConsumerState<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends ConsumerState<LoginForm> {
  final _formKey = GlobalKey<FormBuilderState>();
  bool _senhaOculta = true;
  bool _isLoading = false;

  Future<void> _handleLogin() async {
    final form = _formKey.currentState;
    if (form == null) return;
    if (!form.saveAndValidate()) return;

    setState(() => _isLoading = true);

    final data = form.value;
    final request = LoginRequest(
      email: data['email'],
      password: data['password'],
    );

    final userService = ref.read(userServiceProvider);
    final response = await userService.loginUser(request);

    setState(() => _isLoading = false);

    if (response != null && mounted) {
      context.go('/dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      spacing: 10,
      children: [
        const Logo(),
        FormBuilder(
          key: _formKey,
          child: Column(spacing: 10, children: [
            FormBuilderTextField(
              name: 'email',
              decoration: const InputDecoration(labelText: 'E-mail'),
            ),
            FormBuilderTextField(
              name: 'password',
              obscureText: _senhaOculta,
              decoration: InputDecoration(
                labelText: 'Senha',
                suffixIcon: IconButton(
                  icon: Icon(
                    _senhaOculta ? Icons.visibility : Icons.visibility_off,
                  ),
                  onPressed: () => setState(() => _senhaOculta = !_senhaOculta),
                ),
              ),
            ),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _handleLogin,
                child: Padding(
                  padding: const EdgeInsets.all(2),
                  child: _isLoading
                      ? const CircularProgressIndicator()
                      : const Text('Entrar', style: TextStyle(fontSize: 24)),
                ),
              ),
            ),
          ]),
        ),
      ],
    );
  }
}
