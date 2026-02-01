def ask_int(prompt: str, min_value: int, max_value: int) -> int:
    while True:
        text = input(prompt).strip()

        if not text.isdigit():
            print("Нужно ввести целое число (например 7).")
            continue

        value = int(text)

        if value < min_value or value > max_value:
            print(f"Число должно быть в диапазоне {min_value}..{max_value}.")
            continue

        return value


def ask_name(prompt: str = "Как тебя зовут? ") -> str:
    while True:
        name = input(prompt).strip()
        if len(name) < 2:
            print("Имя слишком короткое. Попробуй ещё раз.")
            continue
        return name
