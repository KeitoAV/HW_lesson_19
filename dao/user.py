from dao.model.user import User


class UserDAO:
    def __init__(self, session) -> None:
        self.session = session

    def get_one(self, uid: int) -> User:
        return self.session.query(User).get(uid)

    def get_all(self) -> list[User]:
        return self.session.query(User).all()

    def create(self, user_d: dict) -> User:
        user = User(**user_d)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, uid: int) -> None:
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d: dict) -> None:
        user = self.get_one(user_d.get("id"))
        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()

    def get_by_username(self, username: str) -> User:
        user = self.session.query(User).filter(User.username == username).one()
        return user
