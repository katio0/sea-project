import re
from pathlib import Path

from sea import Sea, SeaError

IDENTIFIER_PATTERN = r"(?:Sea|море)"
NAME_PATTERN = r"[A-Za-zА-Яа-яЁё]+(?:[ -][A-Za-zА-Яа-яЁё]+)*"
NUMBER_PATTERN = r"[+-]?\d+(?:[.,]\d+)?"
PART_PATTERN = r'"[^"\n]*"|\S+'


def parse_sea(text):
    name = None
    numbers = []
    has_identifier = False
    for part in re.findall(PART_PATTERN, text):
        if re.fullmatch(rf'"\s*{NAME_PATTERN}\s*"', part):
            if name is not None:
                raise SeaError("В строке должно быть только одно название моря")
            name = part[1:-1].strip()
        elif re.fullmatch(NUMBER_PATTERN, part):
            numbers.append(float(part.replace(",", ".")))
        elif re.fullmatch(IDENTIFIER_PATTERN, part, re.IGNORECASE):
            if has_identifier:
                raise SeaError("Допускается один необязательный идентификатор Sea или море")
            has_identifier = True
        else:
            raise SeaError(f"Неверный формат данных: {part}")

    if name is None or len(numbers) != 2:
        raise SeaError(
            'Укажите название в кавычках и два числа: глубину, затем солёность. '
            'Название может стоять в любом месте; Sea или море можно не писать'
        )
    return Sea(name, numbers[0], numbers[1])


def load_seas(file_path):
    seas = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                seas.append(parse_sea(line))
            except SeaError as error:
                print(f"Ошибка в строке {line_number}: {error}. Строка пропущена.")
    return seas


def sort_by_depth(seas):
    return sorted(seas, key=lambda sea: sea.depth)


def print_table(seas):
    if not seas:
        print("Моря не найдены.")
        return
    name_width = max(len("Название моря"), *(len(sea.name) for sea in seas))
    table_header = f"{'Название моря':<{name_width}} | {'Глубина, м':>12} | {'Солёность, ‰':>12}"
    print(f"\nКоличество морей: {len(seas)}")
    print(table_header)
    print("-" * len(table_header))
    for sea in seas:
        print(f"{sea.name:<{name_width}} | {sea.depth:>12g} | {sea.salinity:>12g}")


def run_menu(seas):
    while True:
        print("\nМеню программы «Моря»")
        print("1. Показать таблицу морей")
        print("2. Сортировать моря по глубине")
        print("0. Выход")
        menu_choice = input("Выберите пункт меню: ").strip()
        if menu_choice == "0":
            return
        if menu_choice == "1":
            print_table(seas)
        elif menu_choice == "2":
            print_table(sort_by_depth(seas))
        else:
            print("Такого пункта нет. Выберите 0, 1 или 2.")


def main():
    file_path = Path(__file__).with_name("seas.txt")
    try:
        seas = load_seas(file_path)
    except (OSError, UnicodeError) as error:
        print(f"Не удалось прочитать файл {file_path.name}: {error}")
        return
    try:
        run_menu(seas)
    except (EOFError, KeyboardInterrupt):
        print("\nПрограмма завершена.")


if __name__ == "__main__":
    main()
