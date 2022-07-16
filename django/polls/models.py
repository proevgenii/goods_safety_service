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
        return doc_parser.create_json()


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
