import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:frontend/core/ui/global_toast.dart';
import 'package:frontend/features/auth/models/register.dart';
import 'package:frontend/shared/widgets/layout/logo.dart';
import 'package:form_builder_validators/form_builder_validators.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/features/auth/providers/user_provider.dart';
import 'package:go_router/go_router.dart';

class RegisterForm extends ConsumerStatefulWidget {
  const RegisterForm({super.key});

  @override
  ConsumerState<RegisterForm> createState() => _RegisterFormState();
}

class _RegisterFormState extends ConsumerState<RegisterForm> {
  final _formKey = GlobalKey<FormBuilderState>();
  bool _hideenPass = true;
  bool _hiddenConfirmPass = true;
  bool _isLoading = false;

  Future<void> _handleRegister() async {
    final form = _formKey.currentState;
    if (form == null) return;
    if (!form.saveAndValidate()) return;

    final data = form.value;

    if (data['password'] != data['confirmPassword']) {
      GlobalToast.error('Senhas não coincidem');
      return;
    }

    setState(() => _isLoading = true);

    final request = RegisterRequest(
      nome: data['name'] ?? '',
      email: data['email'] ?? '',
      password: data['password'] ?? '',
    );

    final userService = ref.read(userServiceProvider);
    final response = await userService.registerUser(request);

    setState(() => _isLoading = false);

    if (response != null && mounted) {
      context.go('/dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      spacing: 10,
      mainAxisSize: MainAxisSize.min,
      children: [
        const Logo(),
        FormBuilder(
          key: _formKey,
          child: Column(
            spacing: 10,
            children: [
              FormBuilderTextField(
                name: 'name',
                decoration: const InputDecoration(labelText: 'Nome'),
                inputFormatters: [
                  FilteringTextInputFormatter.allow(RegExp(r'[a-zA-ZÀ-ÿÇç\s]')),
                ],
                validator: FormBuilderValidators.required(
                  errorText: 'Nome é obrigatório',
                ),
              ),
              FormBuilderTextField(
                name: 'email',
                decoration: const InputDecoration(labelText: 'E-mail'),
                validator: FormBuilderValidators.compose([
                  FormBuilderValidators.required(errorText: 'E-mail é obrigatório'),
                  FormBuilderValidators.email(errorText: 'E-mail inválido'),
                ]),
              ),
              Row(
                children: [
                  Expanded(
                    child: FormBuilderTextField(
                      name: 'password',
                      obscureText: _hideenPass,
                      decoration: InputDecoration(
                        labelText: 'Senha',
                        suffixIcon: IconButton(
                          onPressed: () => setState(() => _hideenPass = !_hideenPass),
                          icon: Icon(_hideenPass ? Icons.visibility : Icons.visibility_off),
                        ),
                      ),
                      validator: FormBuilderValidators.required(errorText: 'Senha obrigatória'),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: FormBuilderTextField(
                      name: 'confirmPassword',
                      obscureText: _hiddenConfirmPass,
                      decoration: InputDecoration(
                        labelText: 'Confirmar Senha',
                        suffixIcon: IconButton(
                          onPressed: () => setState(() => _hiddenConfirmPass = !_hiddenConfirmPass),
                          icon: Icon(_hiddenConfirmPass ? Icons.visibility : Icons.visibility_off),
                        ),
                      ),
                      validator: FormBuilderValidators.required(errorText: 'Confirmação obrigatória'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        SizedBox(
          height: 45,
          width: double.infinity,
          child: ElevatedButton(
            onPressed: _isLoading ? null : _handleRegister,
            child: _isLoading
                ? const CircularProgressIndicator()
                : const Text('Registrar'),
          ),
        ),
      ],
    );
  }
}
