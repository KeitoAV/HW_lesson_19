from flask import request
from flask_restx import Resource, Namespace, fields

from dao.model.movie import MovieSchema
from implemented import movie_service, auth_service
from views.directors import director_model
from views.genres import genre_model

movie_ns = Namespace('movies', description='Views for movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# api model
movie_model = movie_ns.model('Movie', {
    'id': fields.Integer(required=False),
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'trailer': fields.String(required=True),
    'year': fields.Integer(required=True),
    'rating': fields.Float(required=True),
    'genre': fields.Nested(required=True, model=genre_model),
    'director': fields.Nested(required=True, model=director_model)
})


@movie_ns.route('/')
@movie_ns.response(200, 'Success', movie_model)
@movie_ns.response(404, 'Not found')
class MoviesView(Resource):
    @movie_ns.doc(description='Get movies')
    @movie_ns.param("genre_id")
    @movie_ns.param("year")
    @movie_ns.param("title")
    @auth_service.auth_required
    def get(self):
        # получить из БД все сущности
        if len(request.args) > 0:
            return movies_schema.dump(movie_service.get_many_filter(**request.args))
        else:
            return movies_schema.dump(movie_service.get_all()), 200

    @movie_ns.doc(description='Add movie')
    @auth_service.admin_required
    def post(self):
        data = movie_schema.load(request.json)
        movie = movie_service.create(data)
        return f"В БД добавлен фильм с ID - {movie.id}", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:mid>')
@movie_ns.response(200, 'Success')
@movie_ns.response(404, 'Not found')
class MovieView(Resource):
    @movie_ns.doc(description='Get movie by ID')
    @auth_service.auth_required
    def get(self, mid: int):
        movie = movie_service.get_one(mid)

        if not movie:
            return f"Фильм с ID - {mid} отсутствует в БД", 404

        return movie_schema.dump(movie), 200

    @movie_ns.doc(description='Update movie by ID')
    @auth_service.admin_required
    def put(self, mid: int):
        data = request.json
        data["id"] = mid
        movie_service.update(data)

        return f"Фильм с ID - {mid} успешно обновлён", 201

    @movie_ns.doc(description='Delete movie by ID')
    @auth_service.admin_required
    def delete(self, mid: int):

        movie = movie_service.get_one(mid)
        if not movie:
            return f"Фильм с ID - {mid} отсутствует в БД", 404

        movie_service.delete(mid)
        return f"Фильм с ID - {mid} удален", 201
