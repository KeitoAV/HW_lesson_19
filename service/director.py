from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, bid):
        """Получить режиссёра по id"""
        return self.dao.get_one(bid)

    def get_all(self):
        """Получить всех режиссёров"""
        return self.dao.get_all()

    def create(self, director_d):
        """Добавление нового режиссёра"""
        return self.dao.create(director_d)

    def update(self, director_d):
        """Обновление данных режиссёра"""
        self.dao.update(director_d)
        return self.dao

    def delete(self, rid):
        """Удаление режиссёра"""
        self.dao.delete(rid)
