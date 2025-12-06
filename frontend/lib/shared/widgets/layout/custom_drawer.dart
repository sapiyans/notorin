import 'package:flutter/material.dart';
import 'dart:ui';

enum DrawerSide { left, right, top, bottom }

class CustomDrawerController {
  _CustomDrawerState? _state;
  
  void open() {
    _state?.openDrawer();
  }
  
  void close() {
    _state?.closeDrawer();
  }
  
  void toggle() {
    _state?.toggleDrawer();
  }
}

class CustomDrawer extends StatefulWidget {
  final Widget? child;
  final Widget? drawerContent;
  final DrawerSide side;
  final double size;
  final double maxBlurIntensity;
  final double maxOverlayOpacity;
  final Duration animationDuration;
  final Curve animationCurve;
  final bool showDragHandle;
  final Color dragHandleColor;
  final double dragHandleThickness;
  final double dragHandleLength;
  final VoidCallback? onOpen;
  final VoidCallback? onClose;
  final CustomDrawerController? controller;

  const CustomDrawer({
    super.key,
    this.child,
    this.drawerContent,
    this.side = DrawerSide.left,
    this.size = 280,
    this.maxBlurIntensity = 5,
    this.maxOverlayOpacity = 0.6,
    this.animationDuration = const Duration(milliseconds: 300),
    this.animationCurve = Curves.easeOutCubic,
    this.showDragHandle = true,
    this.dragHandleColor = Colors.grey,
    this.dragHandleThickness = 7,
    this.dragHandleLength = 150,
    this.onOpen,
    this.onClose,
    this.controller,
  });

  @override
  State<CustomDrawer> createState() => _CustomDrawerState();
}

class _CustomDrawerState extends State<CustomDrawer> {
  bool _isDrawerOpen = false;
  double _dragPosition = 0;
  bool _isDragging = false;

  @override
  void initState() {
    super.initState();
    if (widget.controller != null) {
      widget.controller!._state = this;
    }
  }

  @override
  void dispose() {
    if (widget.controller != null && widget.controller!._state == this) {
      widget.controller!._state = null;
    }
    super.dispose();
  }

  double _getOverlayOpacity() {
    if (!_isDrawerOpen && !_isDragging) return 0;
    
    double progress;
    if (_isDragging) {
      progress = _dragPosition / widget.size;
    } else {
      progress = _isDrawerOpen ? 1 : 0;
    }
    
    return progress * widget.maxOverlayOpacity;
  }

  double _getBlurIntensity() {
    if (!_isDrawerOpen && !_isDragging) return 0;
    
    double progress;
    if (_isDragging) {
      progress = _dragPosition / widget.size;
    } else {
      progress = _isDrawerOpen ? 1 : 0;
    }
    
    return progress * widget.maxBlurIntensity;
  }

  void _toggleDrawer() {
    setState(() {
      _isDrawerOpen = !_isDrawerOpen;
      if (!_isDrawerOpen) {
        _dragPosition = 0;
        widget.onClose?.call();
      } else {
        widget.onOpen?.call();
      }
    });
  }

  void openDrawer() {
    if (!_isDrawerOpen) {
      setState(() {
        _isDrawerOpen = true;
        widget.onOpen?.call();
      });
    }
  }

  void closeDrawer() {
    if (_isDrawerOpen) {
      setState(() {
        _isDrawerOpen = false;
        _dragPosition = 0;
        widget.onClose?.call();
      });
    }
  }

  void toggleDrawer() {
    _toggleDrawer();
  }

  double _getDragDelta(DragUpdateDetails details) {
    switch (widget.side) {
      case DrawerSide.left:
        return details.delta.dx;
      case DrawerSide.right:
        return -details.delta.dx;
      case DrawerSide.top:
        return details.delta.dy;
      case DrawerSide.bottom:
        return -details.delta.dy;
    }
  }

  void _startDrag() {
    setState(() {
      _isDragging = true;
      _dragPosition = _isDrawerOpen ? widget.size : 0;
    });
  }

  void _updateDrag(double delta) {
    setState(() {
      double newPosition = _dragPosition + delta;
      _dragPosition = newPosition.clamp(0.0, widget.size);
    });
  }

  void _endDrag() {
    setState(() {
      _isDragging = false;
      
      bool shouldOpen = _dragPosition > widget.size / 1.15;
      
      if (shouldOpen && !_isDrawerOpen) {
        _isDrawerOpen = true;
        widget.onOpen?.call();
      } else if (!shouldOpen && _isDrawerOpen) {
        _isDrawerOpen = false;
        widget.onClose?.call();
      }
      _dragPosition = 0;
    });
  }

  @override
  Widget build(BuildContext context) {
    double translateX = 0, translateY = 0;
    
    if (!_isDrawerOpen && !_isDragging) {
      switch (widget.side) {
        case DrawerSide.left:
          translateX = -widget.size;
          break;
        case DrawerSide.right:
          translateX = widget.size;
          break;
        case DrawerSide.top:
          translateY = -widget.size;
          break;
        case DrawerSide.bottom:
          translateY = widget.size;
          break;
      }
    } else if (_isDragging) {
      switch (widget.side) {
        case DrawerSide.left:
          translateX = -widget.size + _dragPosition;
          break;
        case DrawerSide.right:
          translateX = widget.size - _dragPosition;
          break;
        case DrawerSide.top:
          translateY = -widget.size + _dragPosition;
          break;
        case DrawerSide.bottom:
          translateY = widget.size - _dragPosition;
          break;
      }
    } else {
      switch (widget.side) {
        case DrawerSide.left:
          translateX = 0;
          break;
        case DrawerSide.right:
          translateX = 0;
          break;
        case DrawerSide.top:
          translateY = 0;
          break;
        case DrawerSide.bottom:
          translateY = 0;
          break;
      }
    }

    Alignment alignment;
    switch (widget.side) {
      case DrawerSide.left:
        alignment = Alignment.centerLeft;
        break;
      case DrawerSide.right:
        alignment = Alignment.centerRight;
        break;
      case DrawerSide.top:
        alignment = Alignment.topCenter;
        break;
      case DrawerSide.bottom:
        alignment = Alignment.bottomCenter;
        break;
    }

    return Stack(
      children: [
        if (widget.child != null) widget.child!,
        
        if (_isDrawerOpen || _isDragging)
          Positioned.fill(
            child: Stack(
              children: [
                AnimatedOpacity(
                  duration: _isDragging ? Duration.zero : widget.animationDuration,
                  opacity: _getOverlayOpacity(),
                  child: Container(
                    color: Colors.black,
                  ),
                ),
                ClipRect(
                  child: BackdropFilter(
                    filter: ImageFilter.blur(
                      sigmaX: _getBlurIntensity(),
                      sigmaY: _getBlurIntensity(),
                    ),
                    child: Container(
                      color: Colors.transparent,
                    ),
                  ),
                ),
                GestureDetector(
                  onTap: _toggleDrawer,
                  child: Container(
                    color: Colors.transparent,
                  ),
                ),
              ],
            ),
          ),
        
        Align(
          alignment: alignment,
          child: AnimatedContainer(
            duration: _isDragging ? Duration.zero : widget.animationDuration,
            curve: widget.animationCurve,
            transform: Matrix4.translationValues(translateX, translateY, 0),
            child: Material(
              elevation: 16,
              child: SizedBox(
                width: (widget.side == DrawerSide.left || widget.side == DrawerSide.right) 
                    ? widget.size 
                    : double.infinity,
                height: (widget.side == DrawerSide.top || widget.side == DrawerSide.bottom) 
                    ? widget.size 
                    : double.infinity,
                child: Stack(
                  children: [
                    Positioned.fill(
                      child: widget.drawerContent ?? Container(),
                    ),
                    if (widget.showDragHandle)
                      _buildDragHandle(),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildDragHandle() {
    Widget handle = MouseRegion(
      cursor: SystemMouseCursors.grab,
      child: GestureDetector(
        onPanStart: (details) => _startDrag(),
        onPanUpdate: (details) => _updateDrag(_getDragDelta(details)),
        onPanEnd: (details) => _endDrag(),
        child: Container(
          decoration: BoxDecoration(
            color: widget.dragHandleColor,
            borderRadius: BorderRadius.circular(3),
          ),
        ),
      ),
    );

    bool isHorizontal = (widget.side == DrawerSide.left || widget.side == DrawerSide.right);
    
    handle = SizedBox(
      width: isHorizontal ? widget.dragHandleThickness : widget.dragHandleLength,
      height: isHorizontal ? widget.dragHandleLength : widget.dragHandleThickness,
      child: handle,
    );

    switch (widget.side) {
      case DrawerSide.left:
        return Align(
          alignment: Alignment.centerRight,
          child: Padding(
            padding: const EdgeInsets.only(right: 2),
            child: handle,
          ),
        );
      case DrawerSide.right:
        return Align(
          alignment: Alignment.centerLeft,
          child: Padding(
            padding: const EdgeInsets.only(left: 2),
            child: handle,
          ),
        );
      case DrawerSide.top:
        return Align(
          alignment: Alignment.bottomCenter,
          child: Padding(
            padding: const EdgeInsets.only(bottom: 2),
            child: handle,
          ),
        );
      case DrawerSide.bottom:
        return Align(
          alignment: Alignment.topCenter,
          child: Padding(
            padding: const EdgeInsets.only(top: 2),
            child: handle,
          ),
        );
    }
  }
}