import pandas as pd
import json

path = """датасет 15072022.xlsx"""
dataset = pd.read_excel(path, sheet_name='датасет', engine = 'openpyxl')
dataset = dataset.loc[~dataset['Технические регламенты'].isna()]
tn_search = pd.read_excel(path, sheet_name='тн вэд поиск', engine = 'openpyxl')
tn_search = tn_search.rename(columns={'Копия Группа продукции.1': 'Группа продукции'})

def get_technical_regulation(dataset) -> dict:
    technical_regulation = dict()
    for k, v in dataset[['Группа продукции', 'Технические регламенты']].values:
        technical_regulation[k] = v
    return technical_regulation

def get_gruppa_and_tov_poz_tn_codes(tn_search) -> dict:
    gruppa_and_tov_poz_tn_codes = dict()
    for k, v in tn_search[['Группа продукции', 'big Коды ТН ВЭД ЕАЭС.1.1']].values:
        gruppa_and_tov_poz_tn_codes[k] = v
    return gruppa_and_tov_poz_tn_codes


with open('technical_regulation.json', 'w') as outfile:
    json.dump(get_technical_regulation(dataset), outfile)

with open('gruppa_and_tov_poz_tn_codes.json', 'w') as outfile:
    json.dump(get_gruppa_and_tov_poz_tn_codes(tn_search), outfile)