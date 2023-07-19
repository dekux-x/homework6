from attrs import define


@define
class Flower:
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        rose = Flower("Rose", 5, 15, 1)
        lily = Flower("Lily", 10, 15, 2)
        bloom = Flower("Bloom", 15, 25, 3)
        self.flowers = []
        self.flowers.append(rose)
        self.flowers.append(lily)
        self.flowers.append(bloom)

    def get_all(self):
        return self.flowers

    def get_by_name(self, name):
        for flower in self.flowers:
            if name == flower.name:
                return flower
        return None

    def get_by_id(self, id):
        for flower in self.flowers:
            if id == flower.id:
                return flower
        return None

    def save(self, flower):
        flower.id = self.get_next_id()
        self.flowers.append(flower)
        return flower

    def get_next_id(self):
        return len(self.flowers) + 1


