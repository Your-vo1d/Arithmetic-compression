import random
from collections import Counter, OrderedDict

def compress(data, compressed_file):
    # Подсчет частоты символов
    freq = {}
    for symbol in data:
        freq[symbol] = freq.get(symbol, 0) + 1
    # Сортировка словаря freq по убыванию частоты и сохранение порядка встречаемости
    sorted_freq = OrderedDict(sorted(freq.items(), key=lambda item: (item[1], data.index(item[0])), reverse=True))

    # Создание вложенных интервалов для каждого символа
    intervals = {}
    low = 0
    high = 65535
    low_last = 0
    high_last = 65535
    bits_F = 0
    
    qtr_1 = int((high_last + 1) / 4)
    half = qtr_1 * 2
    qtr_3 = qtr_1 * 3

    for symbol, count in sorted_freq.items():
        high = low + count
        intervals[symbol] = (low, high)
        low = high
    
    last_key = list(intervals.keys())[-1]
    # Получение значения по последнему ключу
    delit = intervals[last_key][1]
    print(intervals)
    print(intervals['.'][0])
    for symbol in data:
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


comp = "compressed.txt"
data = "КОВ.КОРОВА"
compress(data, comp)
quit()
print("Compressed Data:", compress(data))

