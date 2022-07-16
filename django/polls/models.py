from django.db import models
import os

from polls.ml.doc_parser.doc_parser import ParseDoc
# Create your models here.

PATH = os.path.join("../ml/doc_parser/датасет 15072022.xlsx")
SMOKE = "Извещатель пожарный тепловой линейный ИП104 «Гранат - термокабель», СПР.425212.005 ТУ с изм. 1 «Извещатель пожарный тепловой линейный ИП 104 «Гранат-термокабель». Технические условия», в составе:Чувствительный элемент – термокабель GTSW, варианты исполнения: GTSW – 68, GTSW – 88, GTSW – 105, GTSW – 138, GTSW – 180, GTSW – 68-CP, GTSW – 88-CP, GTSW – 105-CP, GTSW – 138-CP, GTSW – 180-CP"


class OneActivity(models.Model):
    code = models.CharField(max_length=100)
    common_naming = models.TextField(max_length=10000)
    tn_ved = models.TextField(max_length=10000)
    tech_req = models.TextField(max_length=10000)
    group_prod = models.TextField(max_length=10000)
    error = models.CharField(max_length=100)

    def get_results():
        doc_parser = ParseDoc(SMOKE, PATH)
        return doc_parser.create_json()


class TwoActivity(models.Model):
    code = models.CharField(max_length=100)
    common_naming = models.TextField(max_length=10000)
    tn_ved = models.TextField(max_length=10000)
    tech_req = models.TextField(max_length=10000)
    group_prod = models.TextField(max_length=10000)

    def get_results():
        doc_parser = ParseDoc(SMOKE, PATH)
        return doc_parser.create_json()
