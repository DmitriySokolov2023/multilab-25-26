print("=== Рюкзак героя ===")

inventory = []  # список предметов

while True:
    print("\nМЕНЮ:")
    print("1) Показать рюкзак")
    print("2) Добавить предмет")
    print("3) Удалить предмет")
    print("0) Выход")

    choice = input("Выбор: ").strip()

    if choice == "1":
        if len(inventory) == 0:
            print("Рюкзак пуст.")
        else:
            print("В рюкзаке:")
            i = 0
            while i < len(inventory):
                print(i + 1, ")", inventory[i])
                i += 1

    elif choice == "2":
        item = input("Какой предмет добавить? ").strip()
        if item == "":
            print("Пустое название нельзя.")
        else:
            inventory.append(item)
            print("Добавлено:", item)

    elif choice == "3":
        item = input("Какой предмет удалить? ").strip()
        if item in inventory:
            inventory.remove(item)
            print("Удалено:", item)
        else:
            print("Такого предмета нет в рюкзаке.")

    elif choice == "0":
        print("Пока!")
        break

    else:
        print("Нет такой команды.")
