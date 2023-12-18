def compress(data):
    # Подсчет частоты символов
    freq = {}
    for symbol in data:
        freq[symbol] = freq.get(symbol, 0) + 1
    req = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    # Создание интервалов для каждого символа
    intervals = {}
    low = 0
    for symbol, count in req.items():
        high = low + count
        intervals[symbol] = (low, high)
        low = high
    
