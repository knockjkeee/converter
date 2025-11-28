### Установка
___

```bash
  sh setup.sh
```

### Успешный вывод
```text
🛠️ Запуск PyInstaller ./dist/converter/converter [input.json] [output.csv]
✅ Сборка завершена! Исполняемый файл находится в dist/converter/
Тест сборки файла nested.json:
[
  {
    "id": 1,
    "name": "Alice",
    "profile": {
      "age": 30,
      "city": "New York"
    },
    "hobbies": ["reading", "cycling"]
  },
  {
    "id": 2,
    "name": "Bob",
    "profile": {
      "age": 25,
      "city": "London"
    },
    "hobbies": ["gaming", "cooking", "travel"]
  }
]
Process...
Успешно сохранено: output.csv

Результат output.csv:
id,name,hobbies,profile_age,profile_city
1,Alice,"reading, cycling",30,New York
2,Bob,"gaming, cooking, travel",25,London
✅ ГОТОВО
```


### Использование
___

 
```bash
   /dist/converter/converter -in=arg1 -out=arg2 -zab=arg3
 ```
> 
> - arg1 - входной json (input.json )
> - arg2 - обработанный csv (output.csv)
> - arg3 - парсинг шаблона zabbix (true)

#### При использовании только для zabbix, достаточно передавать два аргумента -in=arg1 -zab=arg3. Результат парсинга будет в папке **output**

### Вывод
```text
✅ Сохранено: output/zbx_template_groups.csv (1 записей)
✅ Сохранено: output/zbx_items.csv (43 записей)
✅ Сохранено: output/zbx_triggers.csv (11 записей)
✅ Сохранено: output/zbx_discovery_rules.csv (3 записей)
✅ Сохранено: output/zbx_macros.csv (27 записей)
✅ Сохранено: output/zbx_graphs.csv (8 записей)
✅ Сохранено: output/zbx_dashboards.csv (2 записей)
✅ Сохранено: output/zbx_valuemaps.csv (4 записей)
🏁 Все данные экспортированы в папку 'output/'
```