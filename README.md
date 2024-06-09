## Кодер
Прежде чем перейти к основному методу декодирования, следует обратить внимание конструктору класса ConvolutionalCoder.
Конструктор принимает матрицу, содержащую полиномы, данное решение позволяет нам создавать сверточные коды используя различные полиномы. В конструкторе содержится определение начального состояние, а также создание структуры path_matrix.
Структура path_matrix является контейнером для диаграммы состояний. Для его определения используются методы _where и _code_word
Метод _where принимает состояние и входной бит, затем возвращает состояние, в которое перейдет кодер.
Метод _code_word принимает входной бит и текущее состояние, данный метод возвращает кодовое слово.
Кодирование реализовано в методе encode, метод принимает входные данные, затем инициализирует список для закодированных данных, в цикле перебираются входные символы, затем из структуры path_matrix извлекается кодовое слово, соответствующее данному входному символу, при текущем состоянии, затем сменяется состояние, метод возвращает список содержащий закодированные данные.
## Декодер
Для работы декодера был реализован вспомогательный класс Viterbi_tree.
В конструкторе данного класса объявляются следующие поля:
-	coder (ссылка на объект кодировщика)
-	zero (ссылка на объект решетки, в который ведет текущий объект, в случае получения нулевого входного бита)
-	one (ссылка на объект решетки, в который ведет текущий объект, в случае получения единичного входного бита) 
-	state (состояние объекта)
-	weight (число Хэмминга дуги, ведущей к текущему объекту)
-	code_word (кодовое слово, ведущее к текущему объекту)
Также в конструкторе создаются последующие узлы решетки так, чтобы количество слоев решетки было на единицу больше степени полинома.
Класс Viterbi_tree содержит следующие методы:
estimation – метод, принимает закодированную последовательность и определяется числа Хэмминга для всей решетки
_weighing – данные метод находит вес пути до текущей вершины
choice_better_path – данный метод сравнивает веса путей исходящих из текущей вершины и определяет, какой путь имеет меньший вес
	add_layer – данный метод добавляет новый слой в решетку

	Для декодирования в классе ConvolutionalCoder задан метод decode.
Данный метод принимает закодированные данные, затем создает решетку для алгоритма Витерби. Затем в цикле: в данной решетке подсчитываются числа Хэмминга, выбирается путь с наименьшей суммой данных чисел, декодированный символ добавляется в список для декодированных данных. Далее удаляется слой решетки, в котором путь уже определен, добавляем новый слой, из входных данных удаляется одно кодовое слово. Цикл прервется, когда не останется входных данных. Метод возвращает декодированные данные