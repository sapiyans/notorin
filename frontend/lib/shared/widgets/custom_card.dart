
import 'package:flutter/material.dart';

class CustomCard extends StatelessWidget {
  final Widget child;
  final double? padding;
  
  const CustomCard({
    super.key,
    required this.child,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
          padding: EdgeInsets.all(padding ?? 15),
          child: child,
        )
      );
  }

}