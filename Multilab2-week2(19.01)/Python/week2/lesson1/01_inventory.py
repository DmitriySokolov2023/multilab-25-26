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

    if choice == "2":
      print("Здесь будет логика добавление предмета")
    if choice == "3":
      print("Здесь будет логика удаления предмета")
    if choice == "0":
      print("Выход из программы.")
      break