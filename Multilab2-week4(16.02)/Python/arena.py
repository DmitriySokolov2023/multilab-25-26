import random

player = {
    "name": "Луна",
    "hp": 20,
    "attack": 6,
    "coins": 5,
    "inventory": {"зелье": 1}
}

enemy = {
    "name": "Слизень",
    "hp": 15,
    "attack": 4,
    "reward": 3
}

print("=== АРЕНА ===")
print("Твой герой:", player["name"])
print("Твой враг:", enemy["name"])

while player["hp"] > 0 and enemy["hp"] > 0:
    print("\n--- СТАТУС ---")
    print("Ты:", player["name"], "| HP:", player["hp"], "| Монеты:", player["coins"])
    print("Враг:", enemy["name"], "| HP:", enemy["hp"])

    print("\nМЕНЮ:")
    print("1) Ударить")
    print("2) Выпить зелье (+5 HP)")
    print("3) Пропустить ход (опасно)")
    print("0) Выйти")

    choice = input("Выбор: ").strip()

