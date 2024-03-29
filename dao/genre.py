from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session) -> None:
        self.session = session

    def get_one(self, bid: int) -> Genre:
        return self.session.query(Genre).get(bid)

    def get_all(self) -> list[Genre]:
        return self.session.query(Genre).all()

    def create(self, genre_d: dict) -> Genre:
        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid: int) -> None:
        genre = self.get_one(rid)
        self.session.delete(genre)
        self.session.commit()

    def update(self, genre_d: dict) -> None:
        genre = self.get_one(genre_d.get("id"))
        genre.name = genre_d.get("name")

        self.session.add(genre)
        self.session.commit()
