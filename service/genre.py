from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, bid):
        """Получить жанр по id"""
        return self.dao.get_one(bid)

    def get_all(self):
        """Получить все жанры"""
        return self.dao.get_all()

    def create(self, genre_d):
        """Добавление нового жанра"""
        return self.dao.create(genre_d)

    def update(self, genre_d):
        """Обновление данных жанра"""
        self.dao.update(genre_d)
        return self.dao

    def delete(self, rid):
        """Удаление жанра"""
        self.dao.delete(rid)
