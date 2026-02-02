class Player:
    # Конструктор: вызывается при создании объекта Player(...)
    def __init__(self, name: str, wins: int = 0, losses: int = 0):
        # Поля (атрибуты) объекта:
        self.name = name
        self.wins = wins
        self.losses = losses

    # Метод: действие "победа"
    def win(self) -> None:
        self.wins += 1

    # Метод: действие "поражение"
    def lose(self) -> None:
        self.losses += 1

    # Метод: красивый текст со статистикой
    def stats_text(self) -> None:
      print("\n👤 Игрок:", self.name)
      print("🏆 Побед:", self.wins, "| 💀 Поражений:", self.losses)
      print()

    # Метод: превратить объект в словарь (чтобы сохранить в JSON)
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses
        }

    # Класс-метод: создать объект Player из словаря (который пришёл из JSON)
    @classmethod
    def from_dict(cls, data: dict) -> Player:
        name = data.get("name", "")
        wins = data.get("wins", 0)
        losses = data.get("losses", 0)
        return cls(name=name, wins=wins, losses=losses)
