import random
from collections import Counter, OrderedDict

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
    low = 0
    high = 65_535
    low_last = 0
    high_last = 65_535
    bits_F = 0
    
    qtr_1 = int((high_last + 1) / 4)
    half = qtr_1 * 2
    qtr_3 = qtr_1 * 3
    bits_to_write = []
    delitel = list(table_ranges.values())[-1][1]
    print(delitel)
    
    for symbol in data:
        print(symbol)
        low = int(low_last + table_ranges[symbol][0] * (high_last - low_last + 1) / delitel)
        high = int(low_last + table_ranges[symbol][1] * (high_last - low_last + 1) / delitel - 1)
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
        
def bits_plus_follow(bits_to_write, bits_F, bit):
    bits_to_write.append(bit)
    for i in range(bits_F):
        bits_to_write.append(1 - bit)
comp = "compressed.txt"
data = "КОВ.КОРОВА"
compress(data, comp)
quit()
print("Compressed Data:", compress(data))