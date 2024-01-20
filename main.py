from collections import Counter


def bits_plus_follow(bits_to_write, bits_F, bit):
    bits_to_write.append(bit)
    for i in range(bits_F):
        bits_to_write.append(1 - bit)

def encode(input_file, encode_file):
    data = "КОВ.КОРОВА"
    
    # Подсчет частоты символов
    freq = dict(Counter(data))
    
    sorted_freq = dict(sorted(freq.items(), key=lambda x: (x[1], x[0]), reverse=True))
    #Создание таблицы диапазонов символов
    low = 0
    table_ranges = {}
    for key, value in sorted_freq.items():
        high = low + value
        table_ranges[key] = (low, high)
        low = high
    
    #Переменные для диапазонов low и high
    low = 0
    high = 65_535
    low_last = 0
    high_last = 65_535
    
    #Переменные для хранения половины, четверти
    qtr_1 = int((high_last + 1) / 4)
    half = qtr_1 * 2
    qtr_3 = qtr_1 * 3
    result = []
    delitel = list(table_ranges.values())[-1][1]
    bits_F = 0
    
    for symbol in data:
        low = int(low_last + table_ranges[symbol][0] * (high_last - low_last + 1) / delitel)
        high = int(low_last + table_ranges[symbol][1] * (high_last - low_last + 1) / delitel - 1)

        while True:
            if high < half:
                bits_plus_follow(result, bits_F, 0)
            elif low >= half:
                bits_plus_follow(result, bits_F, 1)
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
        
    result = int(''.join(map(str, result)), 2)
    result = result.to_bytes(4, byteorder='big')
    
    count_chars = len(data)#Подсчет количества элементов в тексте
    count_chars = count_chars.to_bytes(2, byteorder='big')
    #Запись в файл
    with open(encode_file, 'wb') as file:
        #Запись частот символов и словарь символов
        file.write(result)
        file.write(count_chars)
        
        for char, code in sorted_freq.items():
            char_bytes = char.encode('utf-8')
            file.write(len(char_bytes).to_bytes(1, byteorder='big'))
            file.write(char_bytes)
            file.write(value.to_bytes(4, byteorder='big'))  # Записываем частоту символа в 4 байта

def decode(encode_file, decode_file):
    '''
    '''
    
comp = "compressed.txt"
data = "КОВ.КОРОВА"
encode(data, comp)