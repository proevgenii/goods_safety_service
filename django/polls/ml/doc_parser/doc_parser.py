prod_grp_pred = 'Системы передачи извещений о пожаре'

default_code = '9999999'
default_gruppa_tov_poz_tn_codes = '8516'
default_sub_poz_code = '100000'

class ParseDoc:

    def __init__(self, prod_grp_pred: str, tech_reg: dict, gruppa_and_tov_poz: dict, name: str):
        self.prod_grp_pred = prod_grp_pred
        self.technical_regulation = tech_reg
        self.gruppa_and_tov_poz_tn_codes = gruppa_and_tov_poz
        self.sub_poz_code = self.map_sub_poz_code()
        self.name = name

    def map_technical_regulation(self) -> str:
        """This function get product group and searching for the corresponding technical regulation"""
        return self.technical_regulation[self.prod_grp_pred] \
            if self.prod_grp_pred in self.technical_regulation else 0

    def map_gruppa_tov_poz_tn_codes(self) -> str:
        return self.gruppa_and_tov_poz_tn_codes[self.prod_grp_pred] \
            if self.prod_grp_pred in self.gruppa_and_tov_poz_tn_codes else default_gruppa_tov_poz_tn_codes

    def map_sub_poz_code(self) -> str:
        return default_sub_poz_code

    def create_doc(self):
        pass

    def create_yaml(self):
        pass

    def create_json(self):
        file = {'Код': default_code,
                'Общее наименование продукции': self.name,
                'ТН ВЭД ЕАЭС': self.map_gruppa_tov_poz_tn_codes() + self.map_sub_poz_code(),
                'Технические регламенты': self.map_technical_regulation(),
                'Группа продукции': self.prod_grp_pred,
                'Наличие ошибки': 0
                }
        return file