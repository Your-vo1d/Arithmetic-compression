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

    # Кодирование данных
    for symbol in data:
        symbol_range = intervals[symbol]
        range_size = high_last - low_last
        low = low_last + symbol_range[0] * range_size
        high = low_last + symbol_range[1] * range_size

        low_last = int(low)
        high_last = int(high)

    # Вывод результатов
    print("Low:", low_last)
    print("High:", high_last)
compress("КОВ.КОРОВА")

def decomp(data):
    low_last = 0
    high_last = 65_535