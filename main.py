import json
from io_utils import read_items, save_duplicates
from text_processing import combined_similarity, preprocess


def build_word_index(catalog: dict, use_preprocessing: bool = True) -> dict:
    """
    По словам из названия товаров в каталоге строится словарь - для каждого уникального слова из названий товаров хранит
    список ID товаров, где это слово встречается.

    :param catalog:
    :param use_preprocessing:
    :return:
    """
    word_to_ids = {}
    for item_id, name in catalog.items():
        if use_preprocessing:
            name = preprocess(name)
        words = set(name.split())
        for word in words:
            if word not in word_to_ids:
                word_to_ids[word] = []
            word_to_ids[word].append(item_id)
    return word_to_ids


def find_candidates(new_name: str, word_index: dict) -> set:
    """
    Находит множество ID товаров из каталога, которые содержат хотя бы одно общее слово с новым товаром.
    Использует заранее построенный word_index для быстрого отбора кандидатов на сравнение.

    :param new_name:
    :param word_index:
    :param use_preprocessing:
    :return:
    """
    words = set(new_name.split())
    candidate_ids = set()
    for word in words:
        if word in word_index:
            candidate_ids.update(word_index[word])
    return candidate_ids


def find_duplicates(catalog: dict, new_items: dict, threshold: float, use_preprocessing: bool) -> dict:
    """
    Функция поиска дубликатов в каталоге. Сравниваются новые товары только с релевантными кандидатами из каталога.
    Предобработка осуществляется один раз для каждого нового товара, а не при каждом сравнении.
    Вызываются функция вычисления сходства (combined_similarity), проверяется порог сходства. При преодолении порога
    товары, подозрительные на дублирование, добавляются в словарь duplicates.

    :param catalog:
    :param new_items:
    :param threshold:
    :param use_preprocessing:
    :return:
    """
    word_index = build_word_index(catalog, use_preprocessing)

    catalog_preprocessed = {}
    for catalog_id, cat_name in catalog.items():
        catalog_preprocessed[catalog_id] = preprocess(cat_name) if use_preprocessing else cat_name.lower()

    duplicates = {}
    for new_id, new_name in new_items.items():
        new_clean = preprocess(new_name) if use_preprocessing else new_name.lower()

        candidate_ids = find_candidates(new_clean, word_index)

        matches = []
        for cat_id in candidate_ids:
            cat_clean = catalog_preprocessed[cat_id]
            score = combined_similarity(new_clean, cat_clean)
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
