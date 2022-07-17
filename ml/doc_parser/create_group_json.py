import pandas as pd
from collections import defaultdict
import json

dataset = pd.read_excel('датасет 15072022.xlsx', sheet_name='датасет', engine = 'openpyxl')
dataset['Группа продукции'] = dataset['Группа продукции'].astype(str).apply(lambda x: x.strip().split(';'))
dataset = dataset.explode('Группа продукции')

d = defaultdict(list)
for i in range(len(dataset)):
    k, v = dataset[['Группа продукции', 'Коды ТН ВЭД ЕАЭС']].iloc[i]
    v = str(v).split(';')
    k = k.strip()

    for value in v:
        value = value.strip()[:4]
        if value not in d[k]:
            d[k].append(value)

with open('product_group.json', 'w') as outfile:
    json.dump(d, outfile)