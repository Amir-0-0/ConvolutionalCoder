from random import sample


class Viterbi_tree:
    """класс для описания бинарного дерева необходимого для алгоритма Витерби"""
    def __init__(self, coder, state = (0,0), code_word = None, deep = 0 ):
        self.coder = coder
        self.zero = None
        self.one = None
        self.state = tuple(state) # состояние
        self.weight = 0 # число Хэмминга
        self.code_word = code_word
        if deep < len(self.coder.generator_matrix[0]):
            self.zero = Viterbi_tree( coder, *coder.path_matrix[self.state][0], deep + 1)
            self.one = Viterbi_tree( coder, *coder.path_matrix[self.state][1], deep + 1)


    def estimation(self,input_code: list):
        'воспроизводим оценку путей'
        if input_code == [] or not self.one or not self.zero:
            return None
        self.one.weight = 0
        self.zero.weight = 0
        for i, bit in enumerate(input_code[0:2]):
            self.one.weight += int(bit != self.one.code_word[i])
            self.zero.weight += int(bit != self.zero.code_word[i])

        self.one.estimation(input_code[2:])
        self.zero.estimation(input_code[2:])

    def _weighing(self):
        'метод для взвешивания'
        if self.one and self.zero:
            return min(self.one._weighing() , self.zero._weighing()) + self.weight
        return self.weight

    def choice_better_path(self):
        'метод для выбора лучшего пути'
        if self.one._weighing() < self.zero._weighing():
            return 1
        else:
            return 0

    def add_layer(self):
        'метод для добавления слоя'
        if self.one and self.zero:
            self.one.add_layer()
            self.zero.add_layer()
        else:
            self.zero = Viterbi_tree(self.coder, *self.coder.path_matrix[self.state][0], deep=3)
            self.one = Viterbi_tree(self.coder, *self.coder.path_matrix[self.state][1], deep=3)


def noise(data : list, count_of_mistake : int = 1) -> None:
    'функция создающий ошибки принимает последовательность и количество ошибок(по умолчанию 1)'
    for index in sample(range(0,len(data)), count_of_mistake):
        data[index] = 0 if data[index] else 1

class ConvolutionalCoder:

    def __init__(self, generator_matrix):
        self.generator_matrix = generator_matrix
        self.state = [0, 0]  # Начальное состояние регистров

        # словарь содержащий, какие состояния к каким ведут
        self.path_matrix = {
            (0, 0): [[self._where([0,0], 0), self._code_word(0,[0,0])],
                     [self._where([0,0], 1), self._code_word(1,[0,0])]],
            (0, 1): [[self._where([0,1], 0), self._code_word(0,[0,1])],
                     [self._where([0,1], 1), self._code_word(1,[0,1])]],
            (1, 0): [[self._where([1,0], 0), self._code_word(0,[1,0])],
                     [self._where([1,0], 1), self._code_word(1,[1,0])]],
            (1, 1): [[self._where([1,1], 0), self._code_word(0,[1,1])],
                     [self._where([1,1], 1), self._code_word(1,[1,1])]]
        }

    @staticmethod
    def _where(state, bit: int):
        'метод принимает состояние и бит, затем возвращает состояние в которое переходит'
        return [bit] + state[:-1]  # Обновляем состояние регистров

    def _code_word(self, bit: int, state: list):
        'метод принимает бит, затем возвращает кодовое слово'
        output_bits = []  # список для закодированного символа
        for polinom in self.generator_matrix:  # перебираем полиномы
            output_bit = sum(
                [bit * coef for bit, coef in zip([bit] + state, polinom)]) % 2  # считаем выходные биты
            output_bits.append(output_bit)
        return output_bits

    def encode(self, input_data : list) -> list:
        'кодер'
        encoded_data = [] # список для выходной последовательности
        for bit in input_data: # перебираем входные биты
            encoded_data.extend(self.path_matrix[tuple(self.state)][bit][1]) # добавляем кодовое слово в выходную последовательность
            self.state = self._where(self.state, bit)  # Обновляем состояние регистров
        return encoded_data

    def decode(self, input_data: list) -> list:
        'декодер по алгоритму Витерби'
        decode_data = []
        self.state = [0, 0]  # возвращаем состояние в исходное
        root = Viterbi_tree(self) # создаем решетку

        while input_data:
            root.estimation(input_data) # высчитываем веса
            decode_word = root.choice_better_path() # выбираем лучший путь
            decode_data.append(decode_word) # добавляем декодированное слово в вывод
            root = root.one if decode_word else root.zero # сдвигаем сетку
            root.add_layer() # добавляем слой в сетке
            input_data = input_data[2:] # удаляем кодовое слово

        return decode_data

