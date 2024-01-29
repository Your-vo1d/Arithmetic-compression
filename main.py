from collections import Counter
import struct
# Запись указанного бита и отложенных ранее


def bits_plus_follow(bits_to_write, bits_F, bit):

    bits_to_write.append(bit)
    while bits_F > 0:
        bits_to_write.append(1 - bit)
        bits_F -= 1

# Кодирования файла


def encode(input_file, encode_file):

    # Чтение текста с файла
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    # Подсчет частоты символов
    freq = dict(Counter(data))
    # Сортировка словаря частот символов
    sorted_freq = dict(
        sorted(freq.items(), key=lambda x: (x[1], x[0]), reverse=True))
    # Создание таблицы диапазонов символов
    low = 0  # Нижнаяя граница
    table_ranges = {}  # Словарь для хранения символа и его диапазона
    for key, value in sorted_freq.items():
        high = low + value  # Вычисление верхней границы
        table_ranges[key] = (low, high)  # Добавление в словарь
        low = high  # Изменение нижней границы
    # Переменные для диапазонов low и high
    low = 0
    high = 65535

    # Переменные для хранения половины, четверти, третьей части
    qtr_1 = int((high + 1) / 4)  # Первая четверть
    half = qtr_1 * 2  # Половина
    qtr_3 = qtr_1 * 3  # Третья часть

    # Дополнительные переменные
    result = []  # Список с битами результата
    delitel = list(table_ranges.values())[-1][1]  # Делитель
    bits_F = 0  # Количество битов для записи

    # Проход по тексту
    for symbol in data:
        range = (high - low + 1)  # Временная переменная
        # Обновление верхней границы
        high = int(low + table_ranges[symbol][1] * range / delitel - 1)
        # Обновление нижней границы
        low = int(low + table_ranges[symbol][0] * range / delitel) 
        # Нормализация
        while True:
            if (high < half):
                bits_plus_follow(result, bits_F, 0)
            elif low >= half:
                bits_plus_follow(result, bits_F, 1)
                low = low - half
                high = high - half
            elif low >= qtr_3 and high < qtr_1:
                high = high - qtr_1
                low = low - qtr_1
                bits_F += 1
            else:
                break
            low += low
            high += high + 1
    
    bits_F += 1
    if low < qtr_1:
        bits_plus_follow(result, bits_F, 0)
    else:
        bits_plus_follow(result, bits_F, 1)
          
    count_chars = len(data)  # Подсчет количества элементов в тексте
    count_chars = count_chars.to_bytes(2, byteorder='big')
    # Запись в файл
    st = ''.join(map(str, result))
    st = int(st, 2)
    st = st.to_bytes((st.bit_length() + 7) // 8, 'big')
    with open(encode_file, 'wb') as file:
        
        # Запись количества символов в тексте
        file.write(count_chars)
        # Запись словаря частот в таблицу
        for char, code in sorted_freq.items():
            char_bytes = char.encode('utf-8')
            file.write(len(char_bytes).to_bytes(1, byteorder='big'))
            file.write(char_bytes)
            file.write(code.to_bytes(4, byteorder='big'))  # Записываем частоту символа в 4 байта

        # Запись разделителя
        file.write(bytes([0xFF]))
        file.write(len(result).to_bytes(2, byteorder='big'))
        # Запись результата в файл
        file.write(st)
# Декодирование файла


def decode(encode_file, decode_file):
    # Чтение файла и его парсинг
    with open(encode_file, 'rb') as file:
        # Чтение количества символов в тексте
        count_chars = int.from_bytes(file.read(2), byteorder='big')
        # Чтение словаря частот из файла
        sorted_freq = {}
        while True:
            char_len = int.from_bytes(file.read(1), byteorder='big')
            if char_len == 0xFF:  # Проверка на разделитель
                break
            char = file.read(char_len).decode('utf-8')
            code = int.from_bytes(file.read(4), byteorder='big')
            sorted_freq[char] = code

        # Чтение результата из файла
        len_number_list = file.read(2)
        len_number_list = int.from_bytes(len_number_list, byteorder='big')
        number_list = file.read()
        number_list = int.from_bytes(number_list, byteorder='big')
        number_list = [int(bit) for bit in bin(number_list)[2:]]
        while len(number_list) < len_number_list:
            number_list.insert(0, 0)

    # Создание таблицы диапазонов символов
    low = 0  # Нижнаяя граница
    table_ranges = {}  # Словарь для хранения символа и его диапазона
    for key, value in sorted_freq.items():
        high = low + value  # Вычисление верхней границы
        table_ranges[key] = (low, high)  # Добавление в словарь
        low = high  # Изменение нижней границы

    # Переменные для диапазонов low и high
    low = 0
    high = 65535

    delitel = list(table_ranges.values())[-1][1]

    # Переменные для хранения половины, четверти, третьей части
    qtr_1 = int((high + 1) / 4)
    half = qtr_1 * 2
    qtr_3 = qtr_1 * 3

    keys = list(table_ranges.keys())
    keys.insert(0, '-')
    res = list()
    items = [value[0] for value in table_ranges.values()]
    items.append(delitel)
    value_list = number_list[:16]
    number_list = number_list[16:]
    value_string = ''.join(map(str, value_list))  # Преобразование в строку
    result = int(value_string, 2)  # Преобразование в десятичное число
    k = 0

    for i in range(count_chars):
        freq = int(((result - low + 1) * delitel - 1) /
                   (high - low + 1))
        j = 1
        while items[j] <= freq:
            j += 1
        res.append(keys[j])
        
        range_temp = (high - low + 1)  # Временная переменная
        high = int(low + (items[j] * range_temp) / delitel - 1)
        
        low = int(low + (items[j - 1] * range_temp) / delitel)

        
        while True:
            if high < half:
                pass
            elif low >= half:
                result = result - half
                low   = low - half
                high  = high - half
            elif low >= qtr_3 and high < qtr_1:
                high = high - qtr_1
                low = low - qtr_1
                result = result - qtr_1
            else:
                break
            high += high + 1
            low += low
            result += result
            if (k < len(number_list)):
                result += number_list[k]
            k += 1
    res = ''.join(res)
    with open(decode_file, 'w', encoding='utf-8') as file:
        file.write(res)


input_file = "input.txt"
encode_file = "encode.txt"
decode_file = "decode.txt"
encode(input_file, encode_file)
decode(encode_file, decode_file)
encode("test.txt", "result_encode.txt")
decode("result_encode.txt", "result_test.txt")
