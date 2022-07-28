import base64
import hashlib
import hmac

from constants import PWD_ITERATIONS, PWD_SALT
from dao.user import UserDAO
from dao.model.user import User


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_one(self, uid: int) -> User:
        """Получить пользователя id"""
        return self.dao.get_one(uid)

    def get_all(self) -> list[User]:
        """Получить всех пользователей"""
        return self.dao.get_all()

    def create(self, user_d: dict) -> User:
        """Добавление нового пользователя"""
        # hash-пароль
        user_d['password'] = self.generate_password(user_d.get('password'))
        # обновление в базе
        user = self.dao.create(user_d)
        return user

    def update(self, user_d: dict) -> None:
        """Обновление данных пользователя"""
        # hash-пароль
        user_d['password'] = self.generate_password(user_d.get('password'))
        # обновление в базе
        self.dao.update(user_d)

    def delete(self, uid: int) -> None:
        """Удаление пользователя"""
        self.dao.delete(uid)

    def generate_password(self, password: str) -> bytes:
        """Генерация пароля с 'SHA256'"""
        # hash-пароль
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )

        return base64.b64encode(hash_digest)  # b64encode - кодировка с помощью base64 для хранения, возвращает строку

    def get_by_username(self, username: str) -> User:
        """Получение данных пользователя по username"""
        user = self.dao.get_by_username(username)  # ?
        return user

    def compare_passwords(self, password_hash: str, other_password: str) -> bool:
        """Сравнение переданного пароля с паролем пользователя в БД"""

        # декодирование пароля из базы данных
        decoded_digest = base64.b64decode(password_hash)

        # передача hash-пароля
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_SALT,
            PWD_ITERATIONS
        )

        is_equal = hmac.compare_digest(decoded_digest, hash_digest)  # compare_digest() - метод для сравнения паролей

        return is_equal
