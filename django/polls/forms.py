from unittest import result
from django import forms
from django.core import validators
from collections import deque


TEMPLATES = (("ШИНЫ"),
             ("9032"),
             ("Электромагнитная совместимость технических средств"),
             ("Игрушки прочие"),
             ("Конструктор"))


class TestOne(forms.Form):
    code = forms.CharField(max_length=100, initial="Продукция", required=True)
    common_naming = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[0]}), max_length=10000, help_text=TEMPLATES[0], required=True)
    tn_ved = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[1]}), max_length=10000, help_text=TEMPLATES[1], required=True)
    tech_req = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[2]}), max_length=10000, help_text=TEMPLATES[2], required=True)
    group_prod = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[3]}), max_length=10000, help_text=TEMPLATES[3], required=True)
    error = forms.CharField(max_length=100, disabled=True, required=False)


class TestTwo(forms.Form):
    code = forms.CharField(max_length=100, initial="Продукция", required=True)
    common_naming = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[4]}), max_length=300, help_text=TEMPLATES[0], required=True)
    tn_ved = forms.CharField(max_length=100, disabled=True, required=False)
    tech_req = forms.CharField(max_length=100, disabled=True, required=False)
    group_prod = forms.CharField(max_length=100, disabled=True, required=False)


class MapOne(forms.Form):
    def __init__(self, result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = result

        self.fields["code"] = forms.CharField(max_length=100, initial="Продукция" + self.result["Код"], disabled=True, required=True)
        self.fields["common_naming"] = forms.CharField(max_length=10000, initial=self.result["ТН ВЭД ЕАЭС"], disabled=True, required=True)
        self.fields["tn_ved"] = forms.CharField(max_length=10000, initial=self.result["Технические регламенты"], disabled=True, required=True)
        self.fields["tech_req"] = forms.CharField(max_length=10000, initial=self.result["Технические регламенты"], disabled=True, required=True)
        self.fields["group_prod"] = forms.CharField(max_length=10000, initial=self.result["Группа продукции"], disabled=True, required=True)
        self.fields["error"] = forms.CharField(max_length=100, initial=self.result["Наличие ошибки"], disabled=True, required=False)


class MapTwo(forms.Form):
    code = forms.CharField(max_length=100, initial="Продукция", required=True)
    common_naming = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[4]}), max_length=300, help_text=TEMPLATES[0], required=True)
    tn_ved = forms.CharField(max_length=100, disabled=True, required=False)
    tech_req = forms.CharField(max_length=100, disabled=True, required=False)
    group_prod = forms.CharField(max_length=100, disabled=True, required=False)
