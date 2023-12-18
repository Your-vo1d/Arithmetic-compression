import random

def compress(data):
    # Подсчет частоты символов
    freq = {}
    for symbol in data:
        freq[symbol] = freq.get(symbol, 0) + 1
    sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    # Создание вложенных интервалов для каждого символа
    intervals = {}
    low = 0
    high = 2**32
    for symbol, count in sorted_freq.items():
        high = low + count
        intervals[symbol] = (low, high)
        low = high

    # Инициализация границ интервала для кодирования
    low_last = 0
    high_last = 65_535
    qtr_1 = (high_last + 1) / 4
    qtr_3 = qtr_1 * 3
    half = qtr_1 * 2
    bits_break = 0
    
    # Кодирование данных
    for symbol in data:
        symbol_range = intervals[symbol]
        range_size = high_last - low_last
        low = low_last + symbol_range[0] * range_size
        high = low_last + symbol_range[1] * range_size

        low_last = int(low)
        high_last = int(high)
    
    while True:  # Обрабатываем варианты переполнения
        if high_last < half:
            pass
            #Битовая операция
        elif low_last >= half:
            #Битовая операция
            pass
            low_last -= half
            high_last -= half
        elif low_last >= qtr_3 and high_last < qtr_1:
            bits_to_follow += 1
            low_last -= qtr_1
            high_last -= qtr_1
        else:
            break
        low_last += low_last
        high_last += high_last + 1
        
    return low_last, high_last, intervals


