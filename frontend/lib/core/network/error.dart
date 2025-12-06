import 'package:frontend/core/ui/global_toast.dart';

class ErrorHandle {
  ErrorHandle(dynamic e) {
    String message = 'Erro inesperado';

    try {
      final response = e.response;

      if (response != null) {
        final data = response.data;
        if (data is Map && data['error'] != null) {
          final error = data['error'];
          if (error is Map) {
            message = error['message'] ?? message;
          }
        } else if (data is Map && data['detail'] != null) {
          final detail = data['detail'];
          if (detail is String) {
            message = detail;
          } else if (detail is List && detail.isNotEmpty) {
            message = detail.first.toString();
          }
        } else if (data is String) {
          message = data;
        }
      }
    } catch (_) {}

    GlobalToast.error(message);
  }
}
