class Change:
    def __init__(self, value, species):
        self.__value = value  # 0, 1, 2, etc...
        self.__species = species  # 'v', 'w', 'h', None

    @property
    def value(self):
        return self.__value

    @property
    def species(self):
        return self.__species
