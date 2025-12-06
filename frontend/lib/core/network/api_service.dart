import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:frontend/core/ui/global_toast.dart';
import 'package:go_router/go_router.dart';
import 'package:logger/web.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;
  late final Dio _dio;
  final logger = Logger();
  final _storage = const FlutterSecureStorage();

  ApiClient._internal() {
    _dio = Dio(BaseOptions(
      baseUrl: 'http://localhost:8000/api/v1/',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        try {
          final token = await _storage.read(key: 'access_token');
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
        } catch (e) {
          logger.w('Storage read failed in onRequest: $e');
        }
        logger.i('📤 ${options.method} ${options.path}');
        return handler.next(options);
      },
      onResponse: (response, handler) {
        logger.i('📥 ${response.statusCode} ${response.requestOptions.path}');
        return handler.next(response);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          String? refreshToken;
          try {
            refreshToken = await _storage.read(key: 'refresh_token');
          } catch (_) {}

          if (refreshToken != null) {
            try {
              final refreshDio = Dio();
              final refreshResponse = await refreshDio.post(
                '${_dio.options.baseUrl}token/refresh',
                data: {'refresh': refreshToken},
              );
              final newToken = refreshResponse.data['access'];
              if (newToken != null) {
                await _storage.write(key: 'access_token', value: newToken);
                error.requestOptions.headers['Authorization'] = 'Bearer $newToken';
                final retried = await _dio.fetch(error.requestOptions);
                return handler.resolve(retried);
              }
            } catch (_) {}
          }
          try {
            await _storage.deleteAll();
          } catch (_) {}
          GlobalToast.navigatorKey.currentContext?.go('/login');
          return handler.next(error);
        }

        String mensagem = "Erro inesperado";
        if (error.response != null) {
          final data = error.response?.data;
          if (data is Map) {
            if (data['message'] != null) {
              mensagem = data['message'].toString();
            } else if (data['detail'] != null) {
              final detail = data['detail'];
              mensagem = detail is List ? detail.join(', ') : detail.toString();
            } else if (data['error'] is Map && data['error']['message'] != null) {
              mensagem = data['error']['message'].toString();
            }
          } else if (data is String && data.isNotEmpty) {
            mensagem = data;
          }
        }
        logger.e('❌ Dio error: ${error.type} | ${error.message}');
        GlobalToast.error(mensagem);
        return handler.reject(
          error.copyWith(message: '__handled__:$mensagem'),
        );
      },
    ));
  }

  Dio get dio => _dio;

  Future<Response> get(String path, {Map<String, dynamic>? params}) async {
    return await _dio.get(path, queryParameters: params);
  }

  Future<Response> post(String path, {dynamic data}) async {
    return await _dio.post(path, data: data);
  }

  Future<Response> put(String path, {dynamic data}) async {
    return await _dio.put(path, data: data);
  }

  Future<Response> delete(String path) async {
    return await _dio.delete(path);
  }
}
