from flask import request
from flask_restx import Resource, Namespace, fields

from dao.model.genre import GenreSchema
from implemented import genre_service, auth_service

genre_ns = Namespace('genres', description='Views for genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

# api model
genre_model = genre_ns.model('Genre', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True)
})


@genre_ns.route('/')
@genre_ns.response(200, 'Success', genre_model)
@genre_ns.response(404, 'Not found')
class GenresView(Resource):
    @genre_ns.doc(description='Get genres')
    @auth_service.auth_required
    def get(self):
        rs = genre_service.get_all()
        res = genres_schema.dump(rs)
        return res, 200

    @genre_ns.doc(description='Create genre')
    @auth_service.admin_required
    def post(self):
        req_json = request.json
        genre = genre_service.create(req_json)
        return f"В БД добавлен жанр с ID - {genre.id}", 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:rid>')
@genre_ns.response(200, 'Success')
@genre_ns.response(404, 'Not found')
class GenreView(Resource):
    @genre_ns.doc(description='Get genre by ID')
    @auth_service.auth_required
    def get(self, rid: int):
        genre = genre_service.get_one(rid)

        if not genre:
            return f"Жанр с ID - {rid} отсутствует в БД", 404

        return genre_schema.dump(genre), 200

    @genre_ns.doc(description='Update genre by ID')
    @auth_service.admin_required
    def put(self, rid: int):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        genre_service.update(req_json)
        return f"Жанр с ID - {rid} успешно обновлён", 201

    @genre_ns.doc(description='Delete genre by ID')
    @auth_service.admin_required
    def delete(self, rid: int):

        genre = genre_service.get_one(rid)
        if not genre:
            return f"Жанр с ID - {rid} отсутствует в БД", 404

        genre_service.delete(rid)
        return f"Жанр с ID - {rid} удален", 201
