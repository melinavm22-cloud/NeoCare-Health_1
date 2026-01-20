import api from './axios';

// TODO: Cambiar USE_MOCK a false cuando el backend esté listo
const USE_MOCK = false;

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
}

interface RegisterResponse {
  msg: string;
  id: number;
  default_board_id: number;
}

interface User {
  id: number;
  username: string;
  email: string;
}

// Usuario demo para pruebas
const DEMO_USER = {
  email: 'admin@neocare.com',
  password: 'admin123',
  user: { id: 1, username: 'Admin', email: 'admin@neocare.com' }
};

export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  if (USE_MOCK) {
    if (data.email === DEMO_USER.email && data.password === DEMO_USER.password) {
      return Promise.resolve({ access_token: 'mock-token-12345', token_type: 'bearer' });
    }
    throw { response: { data: { detail: 'Credenciales inválidas' } } };
  }
  const response = await api.post<AuthResponse>('/auth/login', data);
  return response.data;
};

export const register = async (data: RegisterRequest): Promise<RegisterResponse> => {
  if (USE_MOCK) {
    return Promise.resolve({ msg: 'Usuario registrado', id: 2, default_board_id: 1 });
  }
  const response = await api.post<RegisterResponse>('/auth/register', data);
  return response.data;
};

export const getMe = async (): Promise<User> => {
  if (USE_MOCK) {
    return Promise.resolve(DEMO_USER.user);
  }
  const response = await api.get<User>('/auth/me');
  return response.data;
};
