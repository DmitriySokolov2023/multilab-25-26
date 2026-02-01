from config import MIN_NUMBER, MAX_NUMBER, MAX_ATTEMPTS
from game import play
from storage import load_data, save_data
from utils import ask_name
from player import Player


def main():
    data = load_data()

    # если имени ещё нет — спросим и сохраним
    if "name" not in data:
        name = ask_name()
        player = Player(name=name)
    else:
        player = Player.from_dict(data)

    player.stats_text()

    # играем один раз
    won = play(MIN_NUMBER, MAX_NUMBER, MAX_ATTEMPTS)

    # обновляем статистику
    if won:
        player.win()
    else:
        player.lose()

    save_data(player.to_dict())
    print("\n💾 Статистика сохранена в save.json")


if __name__ == "__main__":
    main()
