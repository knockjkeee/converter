import pandas as pd
import json
import argparse
import sys

def flatten_and_convert_lists(obj):
  """Рекурсивно не нужен — обработка списков на уровне DataFrame."""
  return obj

def main():
  parser = argparse.ArgumentParser(description="Преобразует JSON-файл в CSV с расплющиванием вложенных структур.")
  parser.add_argument('input_file', help='Путь к входному JSON-файлу')
  parser.add_argument('output_file', help='Путь к выходному CSV-файлу')
  args = parser.parse_args()

  try:
    # Чтение JSON из файла
    with open(args.input_file, 'r', encoding='utf-8') as f:
      data = json.load(f)

    # Проверка: ожидаем список словарей (массив объектов)
    if not isinstance(data, list):
      print("Ошибка: JSON должен содержать массив объектов (список словарей).", file=sys.stderr)
      sys.exit(1)

    # Разглаживание вложенных структур
    df = pd.json_normalize(data, sep='_')

    # Преобразуем списки в строки (например, ["a", "b"] → "a, b")
    for col in df.columns:
      if df[col].apply(lambda x: isinstance(x, list)).any():
        df[col] = df[col].apply(
            lambda x: ', '.join(str(item) for item in x) if isinstance(x, list) else x
        )

    # Сохранение в CSV
    df.to_csv(args.output_file, index=False, encoding='utf-8')
    print(f"Успешно сохранено: {args.output_file}")

  except FileNotFoundError:
    print(f"Ошибка: файл не найден — {args.input_file}", file=sys.stderr)
    sys.exit(1)
  except json.JSONDecodeError as e:
    print(f"Ошибка разбора JSON в файле {args.input_file}: {e}", file=sys.stderr)
    sys.exit(1)
  except Exception as e:
    print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
  main()