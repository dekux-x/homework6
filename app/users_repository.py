from attrs import define


@define
class User:
    email: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        user = User("dias@gmail.com", "dias", "159", 1)
        self.users = []
        self.users.append(user)

    def get_all(self):
        return self.users

    def get_by_email(self, email):
        for user in self.users:
            if email == user.email:
                return user
        return None

    def get_by_id(self, id):
        for user in self.users:
            if id == user.id:
                return user
        return None

    def save(self, user):
        user.id = self.get_next_id()
        self.users.append(user)
        return user

    def get_next_id(self):
        return len(self.users) + 1

