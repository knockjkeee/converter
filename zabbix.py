import json
from pathlib import Path

import pandas as pd


class ZabbixParser:
  def __init__(self, json_file: str, output_dir: str = "output"):
    if json_file is None:
      raise ValueError("Файл для парсинга отсутствует, проверьте флаг -in")
    self.json_file = Path(json_file)
    self.output_dir = Path(output_dir)
    self.output_dir.mkdir(exist_ok=True)
    self.data = None
    self.templates = []

  def load(self):
    with open(self.json_file, 'r', encoding='utf-8') as f:
      self.data = json.load(f)
    if 'zabbix_export' not in self.data:
      raise ValueError("Файл не является Zabbix-экспортом")
    self.templates = self.data['zabbix_export']['templates']
    return self

  def _normalize_and_save(self, records, filename):
    if not records:
      print(f"⚠️ Нет данных для {filename}")
      return
    df = pd.json_normalize(records, sep='_')
    output_path = self.output_dir / filename
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ Сохранено: {output_path} ({len(df)} записей)")

  def export_items(self):
    all_items = []
    for tpl in self.templates:
      items = tpl.get('items', [])
      for item in items:
        item['_template'] = tpl['template']
        item['_name'] = tpl['name']
      all_items.extend(items)
    self._normalize_and_save(all_items, 'zbx_templates_items.csv')

  def export_discovery_rules(self):
    all_discovery = []
    for tpl in self.templates:
      for rule in tpl.get('discovery_rules', []):
        rule['_template'] = tpl['template']
        all_discovery.append(rule)
    self._normalize_and_save(all_discovery, 'zbx_templates_discovery_rules.csv')

  def export_macros(self):
    all_macros = []
    for tpl in self.templates:
      macros = tpl.get('macros', [])
      for m in macros:
        m['_template'] = tpl['template']
      all_macros.extend(macros)
    self._normalize_and_save(all_macros, 'zbx_templates_macros.csv')

  def export_valuemaps(self):
    all_valuemaps = []
    for tpl in self.templates:
      valuemaps = tpl.get('valuemaps', [])
      for m in valuemaps:
        m['_template'] = tpl['template']
      all_valuemaps.extend(valuemaps)
    self._normalize_and_save(all_valuemaps, 'zbx_templates_valuemaps.csv')

  def export_dashboards(self):
    all_dashboards = []
    for tpl in self.templates:
      dashboards = tpl.get('dashboards', [])
      for m in dashboards:
        m['_template'] = tpl['template']
      all_dashboards.extend(dashboards)
    self._normalize_and_save(all_dashboards, 'zbx_templates_dashboards.csv')

  def export_template_groups(self):
    groups = self.data['zabbix_export'].get('template_groups', [])
    self._normalize_and_save(groups, 'zbx_template_groups.csv')

  def export_triggers(self):
    all_triggers = []

    for tpl in self.templates:
      # Глобальные триггеры
      global_triggers = tpl.get('triggers', [])
      for t in global_triggers:
        t['_template'] = tpl['template']
        t['_source'] = 'global'
      all_triggers.extend(global_triggers)

      # Триггеры в items
      for item in tpl.get('items', []):
        for trig in item.get('triggers', []):
          trig['_template'] = tpl['template']
          trig['_source'] = 'item'
          trig['_item_key'] = item['key']
        all_triggers.extend(item.get('triggers', []))

    self._normalize_and_save(all_triggers, 'zbx_templates_items_triggers.csv')

  def export_graphs(self):
    """Извлекает графики."""
    graphs = self.data['zabbix_export'].get('graphs', [])
    self._normalize_and_save(graphs, 'zbx_graphs.csv')

  def export_all(self):

    self.export_template_groups()
    self.export_items()

    self.export_discovery_rules()
    self.export_macros()
    self.export_dashboards()
    self.export_valuemaps()

    self.export_triggers()
    self.export_graphs()
    print("🏁 Все данные экспортированы в папку 'output/'")
