import re


def preprocess(text: str) -> str:
    """
    Функция, предназначенная для предобработки текста перед применением алгоритмов Жаккара и Левенштейна для
    сравнения названия товаров. Здесь происходит нормализация текста (перевод в нижний регистр), замена символов,
    замена предполагаемых ключевых слов на англоязычный перевод (для замены подготовлены наименования, встречавшиеся в
    примере из задания, и цвета, наиболее типичные для техники).
    Далее с помощью регулярных выражений дважды заменяются "гб"/"gb", т. к. это сочетание может встречаться дважды в
    названии, например, смартфона или планшета, а также все символы, кроме букв русского и английского алфавита,
    арабских цифр, символов '+' и '-'. Нормализуются пробелы.

    :param text:
    :return text:
    """
    text = text.lower()

    replacements = {
        "ё": "е",
        "дюйм": "",
        "\"": "",
        "робот-пылесос": "robot vacuum cleaner",
        "телефон": "smartphone",
        "смартфон": "smartphone",
        "планшет": "tablet",
        "часы": "watch",
        "черный": "black",
        "синий": "blue",
        "белый": "white",
        "серый": "grey",
        "серебристый": "silver",
        "золотой": "gold",
        "зеленый": "green",
        "красный": "red"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r'\b(\d+)\s*/\s*(\d+)\s*(?:гб|gb)\b', r'\1/\2', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(\d+)\s*(?:гб|gb)\b', r'\1', text, flags=re.IGNORECASE)

    text = re.sub(r'[^a-zа-я0-9\s/+\-]', ' ', text)

    text = ' '.join(text.split())

    return text


def jaccard_coef(a: str, b: str) -> float:
    """
    Расчитывается коэффициент Жаккара. Он представляет собой отношение числа совпадающих слов из строк a и b к общему
    количеству слов в строках a и b. Данный коэффициент устойчив к перестановкам. Лежит в диапазоне от 0 до 1,
    где 1 - полное совпадение строк.

    :param a:
    :param b:
    :return:
    """
    a_set = set(a.split())
    b_set = set(b.split())
    if not a_set and not b_set:
        return 1.0
    intersection = a_set & b_set
    union = a_set | b_set
    return len(intersection) / len(union)


def levenshtein_distance(a: str, b: str) -> int:
    """
    Расчитывается расстояние Левенштейна. Позволяет подсчитать минимальное количество замен, чтобы слова стали
    одинаковыми. Данная метрика полезна при сравнении слов с опечатками.

    :param a:
    :param b:
    :return:
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1]
                )
    return dp[m][n]


def normalized_levenshtein_distance(a: str, b: str) -> float:
    """
    Нормализованное расстояние Левенштейна. Лежит в диапазоне от 0 до 1, где 1 - полное совпадение строк.
    Нормализация выполняется по формуле:
        similarity = 1 - (levenshtein_distance / max(len(a), len(b)))

    :param a:
    :param b:
    :return:
    """
    dist = levenshtein_distance(a, b)
    max_len = max(len(a), len(b))
    if max_len == 0:
        return 1.0
    return 1.0 - (dist / max_len)


def combined_similarity(a: str, b: str) -> float:
    """
    Вычисляется итоговое сходство по максимальной из двух метрик (коэффициент Жаккара и расстояние Левенштейна).

    :param a:
    :param b:
    :return:
    """
    jaccard = jaccard_coef(a, b)
    levenshtein = normalized_levenshtein_distance(a, b)

    return max(jaccard, levenshtein)
