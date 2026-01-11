# rps_simple.py — Камень-Ножницы-Бумага (очень простой вариант)
# Участник: (ФИО)

import random

# Допустимые ходы: к — камень, н — ножницы, б — бумага
CHOICES = {'к': 'камень', 'н': 'ножницы', 'б': 'бумага'}
# Пары, в которых первый бьёт второго
BEATS = {('к', 'н'), ('н', 'б'), ('б', 'к')}

def ask_player():
    """Запрашивает корректный ввод: к/н/б или q для выхода."""
    while True:
        s = input("Ваш выбор (к/н/б, q — выход): ").strip().lower()
        if s == 'q':
            return 'EXIT'
        if s in CHOICES:
            return s
        print("⚠️ Введите только: к (камень), н (ножницы) или б (бумага).")

def play_once():
    """Играет один раунд и выводит результат."""
    player = ask_player()
    if player == 'EXIT':
        print("Выход из игры.")
        return False  # сигнал завершить общий цикл

    bot = random.choice(list(CHOICES.keys()))
    print(f"Вы: {CHOICES[player]}  |  Бот: {CHOICES[bot]}")

    if player == bot:
        print("Результат: ничья.")
    elif (player, bot) in BEATS:
        print("Результат: вы выиграли!")
    else:
        print("Результат: вы проиграли.")
    return True  # можно продолжать

def main():
    print("Камень-Ножницы-Бумага — простой вариант.")
    while True:
        if not play_once():
            break
        again = input("Сыграть ещё раз? (y/n): ").strip().lower()
        if again != 'y':
            print("До встречи!")
            break

if __name__ == "__main__":
    main()
