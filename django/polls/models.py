from django.db import models
import json
import re
import sys
# Create your models here.


class OneActivity(models.Model):
    code = models.CharField(max_length=100)
    common_naming = models.TextField(max_length=300)
    tn_ved = models.TextField(max_length=300)
    tech_req = models.TextField(max_length=300)
    group_prod = models.TextField(max_length=300)
    error = models.CharField(max_length=100)


class TwoActivity(models.Model):
    code = models.CharField(max_length=100)
    common_naming = models.TextField(max_length=300)
    tn_ved = models.TextField(max_length=300)
    tech_req = models.TextField(max_length=300)
    group_prod = models.TextField(max_length=300)
