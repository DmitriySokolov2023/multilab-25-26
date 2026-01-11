shopping = []
print("Команды: add <товар>, list, remove <№>, exit")

while True:
    raw = input("> ").strip()
    if not raw: 
        continue
    cmd, *rest = raw.split(maxsplit=1)
    cmd = cmd.lower()

    if cmd == "add":
        if not rest: 
            print("Использование: add <товар>"); continue
        item = " ".join(rest[0].split())
        if item: 
            shopping.append(item); print("Добавлено.")
    elif cmd == "list":
        if not shopping: print("(пусто)")
        else:
            for i, name in enumerate(shopping, 1):
                print(f"{i}. {name}")
    elif cmd == "remove":
        if not rest or not rest[0].isdigit():
            print("Использование: remove <номер>"); continue
        i = int(rest[0]) - 1
        if 0 <= i < len(shopping):
            print("Удалено:", shopping.pop(i))
        else:
            print("Нет такого номера.")
    elif cmd == "exit":
        break
    else:
        print("Не знаю такую команду.")
