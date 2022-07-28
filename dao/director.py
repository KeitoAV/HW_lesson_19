from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session) -> None:
        self.session = session

    def get_one(self, bid: int) -> Director:
        return self.session.query(Director).get(bid)

    def get_all(self):
        return self.session.query(Director).all()

    def create(self, director_d: dict) -> Director:
        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid: int) -> None:
        director = self.get_one(rid)
        self.session.delete(director)
        self.session.commit()

    def update(self, director_d: dict) -> None:
        director = self.get_one(director_d.get("id"))
        director.name = director_d.get("name")

        self.session.add(director)
        self.session.commit()
