import random

print("=== Мини-приключение ===")

hp = 10
coins = 5
inventory = []

loot = ["яблоко", "палка", "щит", "зелье"]

while hp > 0:
    print("\n--- СТАТУС ---")
    print("HP:", hp, "| Монеты:", coins, "| В рюкзаке:", len(inventory))

    print("\nМЕНЮ:")
    print("1) Исследовать")
    print("2) Рюкзак")
    print("3) Магазин (зелье = 4 монеты)")
    print("4) Использовать зелье (+5 HP)")
    print("0) Выход")

    choice = input("Выбор: ").strip()

    if choice == "1":
        event = random.randint(1, 3)

        if event == 1:
            item = random.choice(loot)
            inventory.append(item)
            print("Ты нашёл предмет:", item)

        elif event == 2:
            coins += 2
            print("Ты нашёл 2 монеты!")

        else:
            hp -= 2
            print("Ты устал(-а). -2 HP")

    elif choice == "2":
        if len(inventory) == 0:
            print("Рюкзак пуст.")
        else:
            print("В рюкзаке:")
            i = 0
            while i < len(inventory):
                print(i + 1, ")", inventory[i])
                i += 1

    elif choice == "3":
        print("Магазин: зелье стоит 4 монеты.")
        buy = input("Купить зелье? (да/нет): ").strip().lower()
        if buy == "да":
            if coins >= 4:
                coins -= 4
                inventory.append("зелье")
                print("Куплено зелье!")
            else:
                print("Не хватает монет.")

    elif choice == "4":
        if "зелье" in inventory:
            inventory.remove("зелье")
            hp += 5
            print("Ты выпил(а) зелье. +5 HP")
        else:
            print("У тебя нет зелья.")

    elif choice == "0":
        print("Выход из игры.")
        break

    else:
        print("Нет такой команды.")

if hp <= 0:
    print("\nHP стало 0. Игра окончена.")
