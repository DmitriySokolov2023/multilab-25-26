print("=== Рюкзак с количеством (dict) ===")

inventory = {}  # предмет -> количество

while True:
    print("\nМЕНЮ:")
    print("1) Показать рюкзак")
    print("2) Добавить предмет")
    print("3) Использовать предмет")
    print("0) Выход")

    choice = input("Выбор: ").strip()

    if choice == "1":
        if len(inventory) == 0:
            print("Рюкзак пуст.")
        else:
            print("В рюкзаке:")
            # переберём ключи через while по списку ключей
            keys = list(inventory.keys())
            i = 0
            while i < len(keys):
                item = keys[i]
                print(i + 1, ")", item, "-", inventory[item])
                i += 1

    elif choice == "2":
        item = input("Что добавить? ").strip().lower()
        if item == "":
            print("Пустое название нельзя.")
        else:
            if item in inventory:
                inventory[item] = inventory[item] + 1
            else:
                inventory[item] = 1
            print("Добавлено:", item)

    elif choice == "3":
        item = input("Что использовать? ").strip().lower()
        if item in inventory:
            inventory[item] = inventory[item] - 1
            print("Использовано:", item)
            if inventory[item] == 0:
                del inventory[item]
                print(item, "закончился и удалён из рюкзака.")
        else:
            print("Такого предмета нет.")

    elif choice == "0":
        print("Пока!")
        break

    else:
        print("Нет такой команды.")
