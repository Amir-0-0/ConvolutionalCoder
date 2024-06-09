from coder import *

# запасной [1, 0, 1],[1,1,1]
# Пример использования:
generator_matrix = [[0,1,0],[1,1,1]]  # Пример генераторной матрицы для кода R=1/2, m=3

coder = ConvolutionalCoder(generator_matrix)

input_data = [1,1,0,0,0,1,0,1,0,1,0,0,0]  # Пример входных данных
print("входные данные:\n", input_data)
encoded_data = coder.encode(input_data)

print("закодированные данные:\n", encoded_data)
noise(encoded_data, 3) # генерация шума
print("с ошибками:\n", encoded_data)

decode_data =  coder.decode(encoded_data)
print("Декодированные данные:\n" , decode_data)
print(decode_data == input_data)