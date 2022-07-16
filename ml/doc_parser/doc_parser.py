import pandas as pd
import json
# from model import prod_grp_pred # Выход модели Жени


prod_grp_pred = 'Системы передачи извещений о пожаре'
path = 'датасет 15072022.xlsx'
default_code = '9999999'
default_gruppa_tov_poz_tn_codes = '8516'
default_sub_poz_code = '100000'

class ParseDoc:

    def __init__(self, prod_grp_pred: str, path: str):
        self.prod_grp_pred = prod_grp_pred
        self.data = pd.read_excel(path, sheet_name='data')
        self.tn_search = pd.read_excel(path, sheet_name='тн вэд поиск')
        self.tn_search = self.tn_search.rename(columns={'Копия Группа продукции.1': 'Группа продукции'})
        self.dataset = pd.read_excel(path, sheet_name='датасет')
        self.technical_regulation = self.get_technical_regulation(self.dataset)
        self.gruppa_and_tov_poz_tn_codes = self.get_gruppa_and_tov_poz_tn_codes(self.tn_search)
        self.sub_poz_code = self.map_sub_poz_code()

    def map_technical_regulation(self) -> str:
        """This function get product group and searching for the corresponding technical regulation"""
        return self.technical_regulation[self.prod_grp_pred] \
            if self.prod_grp_pred in self.technical_regulation else 0

    def map_gruppa_tov_poz_tn_codes(self) -> str:
        return self.gruppa_and_tov_poz_tn_codes[self.prod_grp_pred] \
            if self.prod_grp_pred in self.gruppa_and_tov_poz_tn_codes else default_gruppa_tov_poz_tn_codes

    def map_sub_poz_code(self) -> str:
        return default_sub_poz_code

    @staticmethod
    def get_technical_regulation(dataset) -> dict:
        technical_regulation = dict()
        for k, v in dataset[['Группа продукции', 'Технические регламенты']].values:
            technical_regulation[k] = v
        return technical_regulation

    @staticmethod
    def get_gruppa_and_tov_poz_tn_codes(tn_search) -> dict:
        gruppa_and_tov_poz_tn_codes = dict()
        for k, v in tn_search[['Группа продукции', 'big Коды ТН ВЭД ЕАЭС.1.1']].values:
            gruppa_and_tov_poz_tn_codes[k] = v
        return gruppa_and_tov_poz_tn_codes

    def create_doc(self):
        pass

    def create_yaml(self):
        pass

    def create_json(self):
        file = {'Код': default_code,
                'Общее наименование продукции': None,
                'ТН ВЭД ЕАЭС': self.map_gruppa_tov_poz_tn_codes() + self.map_sub_poz_code(),
                'Технические регламенты': self.map_technical_regulation(),
                'Группа продукции': self.prod_grp_pred,
                'Наличие ошибки': 0
                }
        return file


if __name__ == 'main':
    doc_parser = ParseDoc(prod_grp_pred, path)
    with open('json_file.txt', 'w') as outfile:
        json.dump(doc_parser.create_json(), outfile)
