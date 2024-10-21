import timeit

# Функції пошуку підрядка

def boyer_moore(text, pattern):
    """Алгоритм Боєра-Мура"""
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    last = {}
    for i in range(m):
        last[pattern[i]] = i
    i = m - 1  # index in text
    j = m - 1  # index in pattern
    while i < n:
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            lo = last.get(text[i], -1)
            i += m - min(j, lo + 1)
            j = m - 1
    return -1

def knuth_morris_pratt(text, pattern):
    """Алгоритм Кнута-Морріса-Пратта"""
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    lps = [0] * m
    compute_lps(pattern, m, lps)
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def compute_lps(pattern, m, lps):
    length = 0
    lps[0] = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

def rabin_karp(text, pattern, q=101):
    """Алгоритм Рабіна-Карпа"""
    d = 256
    m = len(pattern)
    n = len(text)
    p = 0  # hash for pattern
    t = 0  # hash for text
    h = 1
    if m == 0:
        return 0
    for i in range(m-1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return -1

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

file1 = 'article1.txt'
file2 = 'article2.txt'

existing_substring = "if (arr[index] == elementToSearch)"
non_existing_substring = "nonexistent substring"

text1 = read_file(file1)
text2 = read_file(file2)

def measure_time(text, pattern, search_function, label):
    start_time = timeit.default_timer()
    result = search_function(text, pattern)
    elapsed = timeit.default_timer() - start_time
    print(f"{label}: {elapsed:.6f} секунд")
    return elapsed, result

print(f"Пошук у файлі {file1}:")
print("Існуючий підрядок:")
bm_time_existing_1 = measure_time(text1, existing_substring, boyer_moore, "Боєр-Мур")
kmp_time_existing_1 = measure_time(text1, existing_substring, knuth_morris_pratt, "Кнут-Морріс-Пратт")
rk_time_existing_1 = measure_time(text1, existing_substring, rabin_karp, "Рабін-Карп")

print("Неіснуючий підрядок:")
bm_time_non_existing_1 = measure_time(text1, non_existing_substring, boyer_moore, "Боєр-Мур")
kmp_time_non_existing_1 = measure_time(text1, non_existing_substring, knuth_morris_pratt, "Кнут-Морріс-Пратт")
rk_time_non_existing_1 = measure_time(text1, non_existing_substring, rabin_karp, "Рабін-Карп")

print(f"\nПошук у файлі {file2}:")
print("Існуючий підрядок:")
bm_time_existing_2 = measure_time(text2, existing_substring, boyer_moore, "Боєр-Мур")
kmp_time_existing_2 = measure_time(text2, existing_substring, knuth_morris_pratt, "Кнут-Морріс-Пратт")
rk_time_existing_2 = measure_time(text2, existing_substring, rabin_karp, "Рабін-Карп")

print("Неіснуючий підрядок:")
bm_time_non_existing_2 = measure_time(text2, non_existing_substring, boyer_moore, "Боєр-Мур")
kmp_time_non_existing_2 = measure_time(text2, non_existing_substring, knuth_morris_pratt, "Кнут-Морріс-Пратт")
rk_time_non_existing_2 = measure_time(text2, non_existing_substring, rabin_karp, "Рабін-Карп")

print("\nВисновки:")
if bm_time_existing_1[0] < kmp_time_existing_1[0] and bm_time_existing_1[0] < rk_time_existing_1[0]:
    print(f"Для існуючого підрядка в {file1} найшвидший алгоритм: Боєр-Мур")
elif kmp_time_existing_1[0] < bm_time_existing_1[0] and kmp_time_existing_1[0] < rk_time_existing_1[0]:
    print(f"Для існуючого підрядка в {file1} найшвидший алгоритм: Кнут-Морріс-Пратт")
else:
    print(f"Для існуючого підрядка в {file1} найшвидший алгоритм: Рабін-Карп")

