"""Safe console input helpers."""

from typing import Optional


def input_int(
    prompt: str,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
) -> int:
    """Read an integer within optional bounds, retrying invalid input."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")
            continue

        if minimum is not None and value < minimum:
            print(f"Ошибка: число должно быть не меньше {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Ошибка: число должно быть не больше {maximum}.")
            continue
        return value


def input_non_empty(prompt: str) -> str:
    """Read a non-empty text value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")


def input_yes_no(prompt: str) -> bool:
    """Read a yes/no answer in Russian or English."""
    positive_answers = {"да", "д", "yes", "y"}
    negative_answers = {"нет", "н", "no", "n"}
    while True:
        answer = input(prompt).strip().lower()
        if answer in positive_answers:
            return True
        if answer in negative_answers:
            return False
        print("Ошибка: ответьте «да» или «нет».")
