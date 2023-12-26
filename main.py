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
        table_ranges[key] = high
        low = high
    
    # Создание вложенных интервалов для каждого символа
    intervals = {}
    low = 0
    high = 2**32
    low_last = 0
    high_last = 2**32
    bits_F = 0
    
    qtr_1 = int((high_last + 1) / 4)
    half = qtr_1 * 2
    qtr_3 = qtr_1 * 3
    bits_to_write = []
    delitel = list(table_ranges.values())[-1]
    
    for symbol in data:
        low = low_last + intervals[symbol][0] * (high_last - low_last + 1) / delitel
    '''

    delit = intervals[last_key][1]
    print(intervals)
    print(intervals['.'][0])
    s = []
    for symbol in data:
        if symbol not in s:
            s.append(symbol)
            low = int(low_last + intervals[symbol][0] * (high_last - low_last + 1) / delit)
            high = int(low_last + intervals[symbol][1] * (high_last - low_last + 1) / delit - 1)
            print()
            print(low)
            print(high)
            while True:
                if high < half:
                    print("0")
                elif low >= half:
                    print("1")
                    low -= half
                    high -= half
                elif low >= qtr_3 and high < qtr_1:
                    print("FFF")
                    bits_F += 1
                    low -= qtr_1
                    high -= qtr_1
                else:
                    break
                low += low
                high += high + 1

            low_last = int(low)
            high_last = int(high)
            print("Lo "+ str(low_last))
            print("Hi "+ str(high_last))

'''

comp = "compressed.txt"
data = "КОВ.КОРОВА"
compress(data, comp)
quit()
print("Compressed Data:", compress(data))