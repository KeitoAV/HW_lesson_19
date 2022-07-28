from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session) -> None:
        self.session = session

    def get_one(self, mid: int) -> Movie:
        return self.session.query(Movie).get(mid)

    def get_all(self) -> list[Movie]:
        return self.session.query(Movie).all()

    def create(self, data: dict) -> Movie:
        movie = Movie(**data)

        self.session.add(movie)
        self.session.commit()

        return movie

    def update(self, movie: dict) -> None:
        self.session.add(movie)
        self.session.commit()

    def delete(self, mid: int) -> None:
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()

    # получить из БД все сущности
    def get_many_filter_data(self, **kwargs):
        return self.session.query(Movie).filter_by(**{key: value for key, value in kwargs.items() if value is not None
                                                      }).all()
