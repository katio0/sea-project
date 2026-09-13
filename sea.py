class Sea:
    def __init__(self, name, depth, salinity):
        self.name = name
        self.depth = depth
        self.salinity = salinity

    def print_info(self):
        print(f"Название: {self.name}")
        print(f"Глубина: {self.depth} м")
        print(f"Соленость: {self.salinity}")