print("=== Рюкзак героя ===")

inventory = []

while True:
    print("МЕНЮ:")
    print("1) Показать рюкзак")
    print("2) Добавить предмет")
    print("3) Удалить предмет")
    print("0) Выход")
    choice = input("Выберите действие: ").strip()
    if choice == "1":
      if len(inventory) == 0:
        print("Рюкзак пуст.")
      else: 
        print("Содержимое рюкзака:")
        for i in range(len(inventory)):
          print(i+1," - ", inventory[i])

    elif choice == "2":
      item = input('Введите название предмета: ').strip()
      if item == "":
        print('Ввод пустой строки не допускается!')
      else:
        inventory.append(item)
        print(f"Добавлено: {item}")

    elif choice == "3":
      index = int(input('Введи номер предмета.'))
      if index < 0 or index > len(inventory):
        print('Предмета под таким номером не существует!')
      else: del inventory[index - 1]

    elif choice == "0":
      print("Выход из программы.")
      break
    else: print('Вы ввели неверную команду. Можно 1,2,3 или 0')