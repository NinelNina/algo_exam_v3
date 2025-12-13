import json
from io_utils import read_items, save_duplicates
from text_processing import combined_similarity


def find_duplicates(catalog: dict, new_items: dict, threshold: float, use_preprocessing: bool) -> dict:
    """
    Функция поиска дубликатов в каталоге. Сравниваются новые товары из словаря со старыми из словаря-каталога.
    Вызываются функция вычисления сходства (combined_similarity), проверяется порог сходства. При преодолении порога
    товары, подозрительные на дублирование, добавляются в словарь duplicates.

    :param catalog:
    :param new_items:
    :param threshold:
    :param use_preprocessing:
    :return:
    """
    duplicates = {}
    for new_id, new_name in new_items.items():
        matches = []
        for cat_id, cat_name in catalog.items():
            score = combined_similarity(new_name, cat_name, use_preprocessing)
            if score >= threshold:
                matches.append({"catalog_id": cat_id, "similarity_score": round(score, 2)})
        duplicates[new_id] = matches
    return duplicates


if __name__ == '__main__':
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    similarity_threshold = config['SIMILARITY_THRESHOLD']
    use_preprocessing = config['USE_PREPROCESSING']

    catalog = read_items('catalog.txt')
    new_items = read_items('new_items.txt')

    duplicates = find_duplicates(catalog, new_items, similarity_threshold, use_preprocessing)

    save_duplicates(duplicates)
