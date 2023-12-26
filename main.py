from bitarray import bitarray
from collections import Counter, OrderedDict


def bits_plus_follow(bits_to_write, bits_F, bit):
    bits_to_write.append(bit)
    for i in range(bits_F):
        bits_to_write.append(1 - bit)

def compress(data, compressed_file):
    # Подсчет частоты символов
    freq = dict(Counter(data))

    #Сортировка словаря символов по их частоте 
    sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    #Создание таблицы диапазонов символов
    low = 0
    table_ranges = {}
    for key, value in sorted_freq.items():
        high = low + value
        table_ranges[key] = (low, high)
        low = high
    
    # Создание вложенных интервалов для каждого символа
    intervals = {}
    low = 0 #нижнаяя граница
    high = 65_535 #Верхняя граница
    low_last = 0#Предыдущая нижнаяя граница
    high_last = 65_535#Предыдущая верхняя граница
    bits_F = 0#Количество битов для сброса
    
    qtr_1 = int((high_last + 1) / 4) #Первая четверть
    half = qtr_1 * 2 #Половина (середина)
    qtr_3 = qtr_1 * 3# Третья четверть
    bits_to_write = []
    delitel = list(table_ranges.values())[-1][1] #Делитель
    for symbol in data:
        low = int(low_last + table_ranges[symbol][0] * (high_last - low_last + 1) / delitel) #Высчитываем нижнюю границу
        high = int(low_last + table_ranges[symbol][1] * (high_last - low_last + 1) / delitel - 1)#Высчитываем верхнюю границу
        #Минимизация
        while True:
            if high < half:
                bits_plus_follow(bits_to_write, bits_F, 0)
            elif low >= half:
                bits_plus_follow(bits_to_write, bits_F, 1)
                low -= half
                high -= half
            elif low >= qtr_3 and high < qtr_1:
                bits_F += 1
                low -= qtr_1
                high -= qtr_1
            else:
                break
            low += low
            high += high + 1
            
        low_last = int(low)
        high_last = int(high)
    print(bits_to_write)
    with open('output.txt', 'w') as file:
    # Записываем каждый элемент массива в файл
        for element in bits_to_write:
            print(element)
            file.write(str(element) + '\n')

    with open(compressed_file, 'wb') as file:
        
        for char, code in sorted_freq.items():
            char_bytes = char.encode('utf-8')
            file.write(len(char_bytes).to_bytes(1, byteorder='big'))
            file.write(char_bytes)
            file.write(value.to_bytes(4, byteorder='big'))  # Записываем частоту символа в 4 байта

# Пример использования
data = "КОВ.КОРОВА"
compress(data, "compressed_file.txt")

quit()
print("Compressed Data:", compress(data))