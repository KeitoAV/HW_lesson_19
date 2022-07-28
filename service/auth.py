import datetime
import calendar
from typing import Union

import jwt
from flask import request
from flask_restx import abort

from constants import JWT_SECRET, JWT_ALGORITHM
from .user import UserService


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def generate_tokens(self, username: str, password: Union[str, None], is_refresh=False) -> dict:

        """Создание доступа и обновление токенов JWT"""

        # получить пользователя по имени и проверить существование
        user = self.user_service.get_by_username(username)
        if not user:
            abort(404, 'Пользователь не найден')

        # сравнение паролей
        if not is_refresh:
            password_is_correct = self.user_service.compare_passwords(user.password, password)
            if not password_is_correct:
                abort(400, 'Неверный пароль')

        data = {
            'username': user.username,
            'role': user.role
        }

        # генерируем токен доступа (minutes=30)
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # генерируем токен обновления (days=130)
        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token: str) -> dict:
        """Подтверждение токена обновления и создание новой пары токенов"""
        data = jwt.decode(refresh_token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        username = data.get('username')
        return self.generate_tokens(username, None, is_refresh=True)

    @staticmethod
    def auth_required(func):  # декоратор
        """Проверяем правильность переданного токена"""

        def wrapper(*args, **kwargs):
            # проверяем были ли переданы учетные данные авторизации и получаем токен
            if 'Authorization' not in request.headers:
                abort(401, 'Данные авторизации не переданы')

            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]

            # декодирование токена
            try:
                jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception as e:
                abort(401, f'JWT Decode Exception {e}')

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def admin_required(func):  # декоратор
        """Проверка role пользователя"""

        def wrapper(*args, **kwargs):

            if 'Authorization' not in request.headers:
                abort(401)

            data = request.headers["Authorization"]
            token = data.split("Bearer ")[-1]
            # role = None # ?
            # расшифровка токена и проверка role
            try:

                token_decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                role = token_decoded.get("role")
                if role != 'admin':
                    abort(401, 'Role is not admin')
            except Exception as e:
                abort(401, f'JWT Decode Exception {e}')

            return func(*args, **kwargs)

        return wrapper
