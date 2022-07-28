from flask import request
from flask_restx import Resource, Namespace, fields

from dao.model.user import UserSchema
from implemented import user_service, auth_service

user_ns = Namespace('users', description='Views for users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# api model
user_model = user_ns.model('User', {
    'id': fields.Integer(required=False),
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})


@user_ns.route('/')
@user_ns.response(200, 'Success', user_model)
@user_ns.response(404, 'Not found')
class UsersView(Resource):
    @user_ns.doc(description='Get users')
    def get(self):
        users = user_service.get_all()
        res = users_schema.dump(users)
        return res, 200

    @user_ns.doc(description='Add new user')
    def post(self):
        # создание пользователя
        data = request.json
        try:
            user_dict = UserSchema().dump(data)
        except Exception as e:
            return f"{e}", 400
        else:
            user = user_service.create(user_dict)
            return f"В БД добавлен пользователь с ID - {user.id}", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
@user_ns.response(200, 'Success')
@user_ns.response(404, 'Not Found')
class UserView(Resource):
    @user_ns.doc(description='Get user by id')
    def get(self, uid: int):
        user = user_service.get_one(uid)
        if not user:
            return f"Пользователь с ID - {uid} отсутствует в БД", 404

        return user_schema.dump(user), 200

    @user_ns.doc(description='Update user by id')
    def put(self, uid: int):

        user = user_service.get_one(uid)
        if not user:
            return f"Пользователь с ID - {uid} отсутствует в БД", 404

        data = request.json
        if "id" not in data:
            data["id"] = uid

        user_service.update(data)
        return f"Пользователь с ID - {uid} успешно обновлён", 201

    @user_ns.doc(description='Delete user by id')
    # @auth_service.admin_required
    def delete(self, uid: int):

        user = user_service.get_one(uid)
        if not user:
            return f"Пользователь с ID - {uid} отсутствует в БД", 404

        user_service.delete(uid)
        return f"Пользователь с ID - {uid} удален", 204
