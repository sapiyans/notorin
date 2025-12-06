class RegisterRequest {
  final String nome;
  final String email;
  final String password;

  RegisterRequest({
    required this.nome,
    required this.email,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'nome': nome,
      'email': email,
      'password': password,
    };
  }
}

class LoginRequest {
  final String email;
  final String password;

  LoginRequest({required this.email, required this.password});

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'password': password,
    };
  }
}

class UserResponse {
  final int id;
  final String? lastLogin;
  final bool isSuperUser;
  final String username;
  final String firstName;
  final String lastName;
  final String email;
  final bool isStaff;
  final bool isActive;
  final String dateJoined;
  final List<dynamic> groups;
  final List<dynamic> userPermissions;

  UserResponse({
    required this.id,
    this.lastLogin,
    required this.isSuperUser,
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.email,
    required this.isStaff,
    required this.isActive,
    required this.dateJoined,
    required this.groups,
    required this.userPermissions,
  });

  factory UserResponse.fromJson(Map<String, dynamic> json) {
    return UserResponse(
      id: json['id'] as int,
      lastLogin: json['last_login'] as String?,
      isSuperUser: json['is_superuser'] as bool? ?? false,
      username: json['username'] as String? ?? '',
      firstName: json['first_name'] as String? ?? '',
      lastName: json['last_name'] as String? ?? '',
      email: json['email'] as String? ?? '',
      isStaff: json['is_staff'] as bool? ?? false,
      isActive: json['is_active'] as bool? ?? true,
      dateJoined: json['date_joined'] as String? ?? '',
      groups: json['groups'] as List<dynamic>? ?? [],
      userPermissions: json['user_permissions'] as List<dynamic>? ?? [],
    );
  }
}
