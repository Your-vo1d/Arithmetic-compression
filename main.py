from collections import Counter


def compress(input_file, compressed_file):
    #Чтение текста
    with open(input_file, 'r', encoding='utf-8') as file:
        #Получение текста с файла
        text = file.read()
         
    #Словарь частот символов в тексте    
    freq = dict(Counter(text))

    #Сортировка словаря символов по их частоте 
    sorted_freq = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))
    
    low = 0
    low_last = 0
    high = 2 ** 32 - 1
    high_last = 2 ** 32 - 1
    
    for symbol in text:
        range = (high_last - low_last + 1)
        low = low_last + b * range / delitel
        high = low_last + b * range / delitel - 1
    
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

def decompress(compressed_file, decoded_file):
    with open(compressed_file, 'rb') as file:
        