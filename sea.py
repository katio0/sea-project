import math


class SeaError(ValueError):
    """Ошибка в данных моря или диапазоне солёности."""


class Sea:
    def __init__(self, name, depth, salinity):
        if not isinstance(name, str) or not name.strip():
            raise SeaError("Название моря не может быть пустым")
        self.validate_number(depth, "Глубина")
        self.validate_number(salinity, "Солёность")
        self.name = name
        self.depth = depth
        self.salinity = salinity

    @staticmethod
    def validate_number(number, field_name):
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise SeaError(f"{field_name}: требуется число")
        if not math.isfinite(number):
            raise SeaError(f"{field_name}: требуется конечное число")
        if number < 0:
            raise SeaError(f"{field_name} не может быть отрицательной")

    def __str__(self):
        return (
            f"Название: {self.name}\n"
            f"Глубина: {self.depth:g} м\n"
            f"Солёность: {self.salinity:g} ‰"
        )
