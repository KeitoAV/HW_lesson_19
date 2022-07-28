from dao.model.movie import Movie
from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        """Получить фильм по id"""
        return self.dao.get_one(mid)

    def get_all(self) -> list[Movie]:
        """Получить все фильмы"""
        return self.dao.get_all()

    def create(self, data):
        """Добавление нового фильма"""
        return self.dao.create(data)

    def update(self, data):
        """Обновление данных фильма"""
        mid = data.get("id")
        movie = self.get_one(mid)

        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")
        movie.genre = data.get("genre")
        movie.director = data.get("director")

        self.dao.update(movie)
        return movie

    def delete(self, mid):
        """Удаление фильма"""
        self.dao.delete(mid)

    def get_many_filter(self, **kwargs):
        """Получить из БД все сущности"""
        return self.dao.get_many_filter_data(**kwargs)
