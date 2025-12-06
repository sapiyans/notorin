import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:frontend/core/network/api_service.dart';
import 'package:frontend/core/network/error.dart';
import 'package:frontend/features/auth/models/register.dart';
import 'package:frontend/core/ui/global_toast.dart';

class UserLoginService {
  static final UserLoginService _instance = UserLoginService._internal();

  factory UserLoginService() => _instance;
  UserLoginService._internal();

  final ApiClient _apiClient = ApiClient();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<UserResponse?> registerUser(RegisterRequest request) async {
    try {
      final response = await _apiClient.post('user/register', data: request.toJson());
      final rawData = response.data as Map<String, dynamic>;
      await _saveAuthData(rawData);
      GlobalToast.success('Usuário registrado com sucesso!');
      return UserResponse.fromJson(rawData['user'] as Map<String, dynamic>? ?? rawData);
    } catch (e) {
      _handleError(e);
      return null;
    }
  }

  Future<UserResponse?> loginUser(LoginRequest request) async {
    try {
      final response = await _apiClient.post('user/login', data: request.toJson());
      final rawData = response.data as Map<String, dynamic>;
      await _saveAuthData(rawData);
      GlobalToast.success('Login realizado com sucesso!');
      return UserResponse.fromJson(rawData['user'] as Map<String, dynamic>? ?? rawData);
    } catch (e) {
      _handleError(e);
      return null;
    }
  }

  Future<bool> refreshToken() async {
    try {
      final token = await _storage.read(key: 'refresh_token');
      if (token == null) return false;

      final response = await _apiClient.post(
        'token/refresh',
        data: {'refresh': token},
      );

      if (response.data['access'] != null) {
        await _storage.write(key: 'access_token', value: response.data['access']);
        return true;
      }
      return false;
    } catch (_) {
      return false;
    }
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }

  Future<String?> getAccessToken() async {
    return _storage.read(key: 'access_token');
  }

  Future<Map<String, dynamic>?> getCurrentUser() async {
    final userData = await _storage.read(key: 'user_data');
    if (userData == null) return null;
    return jsonDecode(userData);
  }

  Future<void> logout() async {
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
    await _storage.delete(key: 'user_data');
    GlobalToast.success('Logout realizado com sucesso!');
  }

  Future<void> _saveAuthData(Map<String, dynamic> data) async {
    if (data['access'] != null) {
      await _storage.write(key: 'access_token', value: data['access']);
    }
    if (data['refresh'] != null) {
      await _storage.write(key: 'refresh_token', value: data['refresh']);
    }
    if (data['user'] != null) {
      await _storage.write(key: 'user_data', value: jsonEncode(data['user']));
    }
  }

  void _handleError(dynamic e) {
    final isHandled = e is DioException && (e.message?.startsWith('__handled__') ?? false);
    if (!isHandled) ErrorHandle(e);
  }
}
