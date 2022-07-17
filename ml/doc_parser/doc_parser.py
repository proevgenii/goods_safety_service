import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

prod_grp_pred = 'Системы передачи извещений о пожаре'
name = 'Шины'
default_code = '9999999'
default_gruppa_tov_poz_tn_codes = '8516'
default_sub_poz_code = '100000'

class ParseDoc:

    def __init__(self, prod_grp_pred: str, tech_reg: dict, product_group: dict, name: str, tnved4):
        self.prod_grp_pred = prod_grp_pred
        self.technical_regulation = tech_reg
        self.name = name
        self.tnved4 = tnved4
        self.product_group = product_group

    def map_technical_regulation(self) -> str:
        """This function get product group and searching for the corresponding technical regulation"""
        return self.technical_regulation[self.prod_grp_pred] \
            if self.prod_grp_pred in self.technical_regulation else 0

    def map_tn_code(self):
        predictions_list = []
        for code in self.product_group[self.prod_grp_pred]:
            if code == 'nan':
                continue
            gruppa = int(code[:2])
            poz = int(code[2:5])
            description = self.tnved4.loc[(self.tnved4['119'] == gruppa) &
                                          (self.tnved4['20220113'] == poz)]['Unnamed: 3']
            predict = process.extract(self.name, description, limit=1)
            predictions_list.append(predict)

        predictions_list.sort(key=lambda x: x[0][1])
        return ''.join(list(map(str, self.tnved4.iloc[predictions_list[-1][0][2]].values[0:3].tolist())))

    def create_doc(self):
        pass

    def create_yaml(self):
        pass

    def create_json(self):
        file = {'Код': default_code,
                'Общее наименование продукции': self.name,
                'ТН ВЭД ЕАЭС': self.map_tn_code(),
                'Технические регламенты': self.map_technical_regulation(),
                'Группа продукции': self.prod_grp_pred,
                'Наличие ошибки': 0
                }
        return file


with open('technical_regulation.json') as f:
    file_content = f.read()
    tech_reg= json.loads(file_content)

with open('product_group.json') as f:
    file_content = f.read()
    product_group = json.loads(file_content)

tnved4 = pd.read_table('TNVED4.Txt', sep='|', encoding='cp866', index_col=False)
parser = ParseDoc(prod_grp_pred, tech_reg, product_group, name, tnved4=tnved4)
print(parser.create_json())