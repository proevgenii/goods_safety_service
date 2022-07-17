from django.db import models
import os
import json

from polls.ml.doc_parser.doc_parser import ParseDoc
from polls.ml.group_predict import predict_baseline
# Create your models here.

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join("../ml/doc_parser/датасет 15072022.xlsx")
GROUP_PATH = os.path.join(PATH, "ml", "doc_parser",
                          "gruppa_and_tov_poz_tn_codes.json")
TECH_PATH = os.path.join(PATH, "ml", "doc_parser", "technical_regulation.json")
SMOKE = "Извещатель пожарный тепловой линейный ИП104 «Гранат - термокабель», СПР.425212.005 ТУ с изм. 1 «Извещатель пожарный тепловой линейный ИП 104 «Гранат-термокабель». Технические условия», в составе:Чувствительный элемент – термокабель GTSW, варианты исполнения: GTSW – 68, GTSW – 88, GTSW – 105, GTSW – 138, GTSW – 180, GTSW – 68-CP, GTSW – 88-CP, GTSW – 105-CP, GTSW – 138-CP, GTSW – 180-CP"


with open(TECH_PATH) as f:
    file_content = f.read()
    TECH: dict = json.loads(file_content)


with open(GROUP_PATH) as f:
    file_content = f.read()
    GROUP = json.loads(file_content)


class OneActivity(models.Model):
    code = models.CharField(max_length=100)
    common_naming = models.TextField(max_length=10000)
    tn_ved = models.TextField(max_length=10000)
    tech_req = models.TextField(max_length=10000)
    group_prod = models.TextField(max_length=10000)
    error = models.CharField(max_length=100)

    def get_results(self):
        prod_grp_pred = predict_baseline(self.common_naming)['prod_group']
        doc_parser = ParseDoc(prod_grp_pred, TECH, GROUP, self.common_naming)
        result = doc_parser.create_json()
        #TODO delete this:
        result = {'Код': "37632",
                  'Общее наименование продукции': "Проходки кабельные модульные универсальные огнестойкие типа КП-90, габаритными размерами 580х540 мм, общей толщиной 320 мм, состоящие из стальной рамки из угловых профилей(ГОСТ 8509-86), 8 закрепительных анкерных пластин(ГОСТ 8509-86), уплотнительных огнестойких модулей с цельнорезиновым сердечником типа РМ(глубиной 60 мм с каждой стороны) и компрессионных блоков типа РВ(глубиной 60 мм с каждой стороны). Пространство 200 мм между двумя проходками заполнено минеральной ватой плотностью не менее 90 кг/м3. Изготавливаются в соответствии с Техническими условиями ТУ 3464-001-49247031-2016 с изм. № 1 «Проходки кабельные модульные универсальные огнестойкие».",
                  'ТН ВЭД ЕАЭС': "4016999708",
                  'Технические регламенты': "ТР ЕАЭС 043/2017 О требованиях к средствам обеспечения пожарной безопасности и пожаротушения",
                  'Группа продукции': "Узлы пересечения противопожарных преград кабельными изделиями, шинопроводами, герметичными кабельными вводами, муфтами и трубопроводами инженерных систем зданий и сооружений",
                  'Наличие ошибки': 0
                  }

        if self.tn_ved != result["ТН ВЭД ЕАЭС"]:
            result["Наличие ошибки"] = 11
        if self.tech_req != result["Технические регламенты"] and result["Технические регламенты"] != "not_found":
            result["Наличие ошибки"] = 12
        if self.group_prod != result["Группа продукции"]:
            result["Наличие ошибки"] = 13

        if self.tn_ved != result["ТН ВЭД ЕАЭС"] and self.tech_req != result["Технические регламенты"] and result["Технические регламенты"] != "not_found":
            result["Наличие ошибки"] = 14
        if self.tn_ved != result["ТН ВЭД ЕАЭС"] and self.group_prod != result["Группа продукции"]:
            result["Наличие ошибки"] = 15
        if self.tech_req != result["Технические регламенты"] and result["Технические регламенты"] != "not_found" and self.group_prod != result["Группа продукции"]:
            result["Наличие ошибки"] = 16

        if self.tn_ved != result["ТН ВЭД ЕАЭС"] and self.tech_req != result["Технические регламенты"] and result["Технические регламенты"] != "not_found" and self.group_prod != result["Группа продукции"]:
            result["Наличие ошибки"] = 17

        return result


class TwoActivity(models.Model):
    code = models.CharField(max_length=100)
    common_naming = models.TextField(max_length=10000)
    tn_ved = models.TextField(max_length=10000)
    tech_req = models.TextField(max_length=10000)
    group_prod = models.TextField(max_length=10000)

    def get_results(self):
        prod_grp_pred = predict_baseline(self.common_naming)['prod_group']
        doc_parser = ParseDoc(prod_grp_pred, TECH, GROUP, self.common_naming)
        return doc_parser.create_json()
