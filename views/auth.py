from flask import request
from flask_restx import Resource, Namespace, fields

from implemented import auth_service

auth_ns = Namespace('auth', description='Views for auth')

# api models
auth_model = auth_ns.model('Authentication', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

tokens_model = auth_ns.model('Tokens', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})


@auth_ns.route('/')
class AuthView(Resource):
    @auth_ns.doc(description='User authorization', body=auth_model)
    @auth_ns.response(201, 'Tokens created', tokens_model)
    @auth_ns.response(400, 'Not Found')
    def post(self):
        # авторизация пользователя
        data = request.json

        username = data.get('username', None)
        password = data.get('password', None)
        if None in [username, password]:
            return "Не удалось авторизоваться", 400

        # генерация токенов
        tokens = auth_service.generate_tokens(username, password)

        return tokens, 201

    @auth_ns.doc(description='Update token by user')
    @auth_ns.response(201, 'Tokens updated', tokens_model)
    @auth_ns.response(404, 'Not Found')
    def put(self):
        # обновление hash-пароля пользователя
        data = request.json
        refresh_token = data.get('refresh_token')
        tokens = auth_service.approve_refresh_token(refresh_token)
        return tokens, 201
