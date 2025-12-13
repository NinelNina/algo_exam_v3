import json


def read_items(filename: str) -> dict:
    """
    Чтение товаров из файла.

    :param filename:
    :return:
    """
    items = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
            item_id, name = parts
            items[item_id] = name
    return items


def save_duplicates(duplicates: dict, filename: str = 'duplicates.json'):
    """
    Сохранение дубликатов в duplicates.json.

    :param duplicates:
    :param filename:
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(duplicates, f, ensure_ascii=False, indent=2)
