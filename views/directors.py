from flask import request
from flask_restx import Resource, Namespace, fields

from dao.model.director import DirectorSchema
from implemented import director_service, auth_service

director_ns = Namespace('directors', description='Views for directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

# api model
director_model = director_ns.model('Director', {
    'id': fields.Integer(required=False),
    'name': fields.String(required=True)
})


@director_ns.route('/')
@director_ns.response(200, 'Success', director_model)
@director_ns.response(404, 'Not found')
class DirectorsView(Resource):
    @director_ns.doc(description='Get directors')
    @auth_service.auth_required
    def get(self):
        rs = director_service.get_all()
        res = directors_schema.dump(rs)
        return res, 200

    @director_ns.doc(description='Create director')
    @auth_service.admin_required
    def post(self):
        req_json = request.json
        director = director_service.create(req_json)
        return f"В БД добавлен режиссер с ID - {director.id}", 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:rid>')
@director_ns.response(200, 'Success')
@director_ns.response(404, 'Not found')
class DirectorView(Resource):
    @director_ns.doc(description='Get director by ID')
    @auth_service.auth_required
    def get(self, rid: int):
        director = director_service.get_one(rid)

        if not director:
            return f"Режиссер с ID - {rid} отсутствует в БД", 404

        return director_schema.dump(director), 200

    @director_ns.doc(description='Update director by ID')
    @auth_service.admin_required
    def put(self, rid: int):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = rid
        director_service.update(req_json)
        return f"Режиссер с ID - {rid} успешно обновлён", 201

    @director_ns.doc(description='Delete director by ID')
    @auth_service.admin_required
    def delete(self, rid: int):

        director = director_service.get_one(rid)
        if not director:
            return f"Режиссер с ID - {rid} отсутствует в БД", 404

        director_service.delete(rid)

        return f"Режиссер с ID - {rid} удален", 201
