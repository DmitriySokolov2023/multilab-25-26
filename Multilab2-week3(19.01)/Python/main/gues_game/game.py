import random
from utils import ask_int


def play(min_number: int, max_number: int, max_attempts: int) -> bool:
    secret = random.randint(min_number, max_number)
    attempts_left = max_attempts

    print(f"Я загадал число от {min_number} до {max_number}.")
    print(f"У тебя {max_attempts} попыток!")

    while attempts_left > 0:
        guess = ask_int("Твой вариант: ", min_number, max_number)
        attempts_left -= 1

        if guess == secret:
            print("✅ Угадал!")
            return True

        if guess < secret:
            print("⬆️ Больше!")
        else:
            print("⬇️ Меньше!")

        print("Осталось попыток:", attempts_left)

    print(f"❌ Попытки закончились. Я загадал: {secret}")
    return False
