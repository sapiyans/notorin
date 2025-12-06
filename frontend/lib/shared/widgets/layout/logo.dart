import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class Logo extends StatelessWidget {
  const Logo({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(Icons.note, size: 55, color: theme.colorScheme.primary),
        GestureDetector(
          onTap: () => context.goNamed('dashboard'),
          child:Text(
          'Notorin',
            style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
          ),
        )
      ],

    );}
}