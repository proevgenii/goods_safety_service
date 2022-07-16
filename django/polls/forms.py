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
        widget=forms.Textarea(attrs={'placeholder': TEMPLATES[4]}), max_length=10000, help_text=TEMPLATES[0], required=True)
    tn_ved = forms.CharField(max_length=100, disabled=True, required=False)
    tech_req = forms.CharField(max_length=100, disabled=True, required=False)
    group_prod = forms.CharField(max_length=100, disabled=True, required=False)


class MapOne(forms.Form):
    def __init__(self, result, user_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = result
        self.user_data = user_data
        print(self.user_data)
        self.label_1, self.label_2, self.label_3 = "Ошибок нет", "Ошибок нет", "Ошибок нет"
        if self.result["Наличие ошибки"] == 11:
            self.label_1 = f'Неверно введённый ТН ВЭД ЕАЭС: {self.user_data["tn_ved"]}'
        elif self.result["Наличие ошибки"] == 12:
            self.label_2 = f'Неверно введённые технические регламенты: {self.user_data["tech_req"]}'
        elif self.result["Наличие ошибки"] == 13:
            self.label_3 = f'Неверно введённая группа продукции: {self.user_data["group_prod"]}'
        elif self.result["Наличие ошибки"] == 14:
            self.label_1 = f'Неверно введённый ТН ВЭД ЕАЭС: {self.user_data["tn_ved"]}'
            self.label_2 = f'Неверно введённые технические регламенты: {self.user_data["tech_req"]}'
        elif self.result["Наличие ошибки"] == 15:
            self.label_1 = f'Неверно введённый ТН ВЭД ЕАЭС: {self.user_data["tn_ved"]}'
            self.label_3 = f'Неверно введённая группа продукции: {self.user_data["group_prod"]}'
        elif self.result["Наличие ошибки"] == 16:
            self.label_2 = f'Неверно введённые технические регламенты: {self.user_data["tech_req"]}'
            self.label_3 = f'Неверно введённая группа продукции: {self.user_data["group_prod"]}'
        elif self.result["Наличие ошибки"] == 17:
            self.label_1 = f'Неверно введённый ТН ВЭД ЕАЭС: {self.user_data["tn_ved"]}'
            self.label_2 = f'Неверно введённые технические регламенты: {self.user_data["tech_req"]}'
            self.label_3 = f'Неверно введённая группа продукции: {self.user_data["group_prod"]}'


        self.fields["code"] = forms.CharField(
            max_length=100, initial="Продукция " + self.result["Код"], disabled=True, required=True)
        self.fields["common_naming"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["Общее наименование продукции"], disabled=True, required=True)

        self.fields["tn_ved"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["ТН ВЭД ЕАЭС"], disabled=True, required=True, label = self.label_1)

        self.fields["tech_req"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["Технические регламенты"], disabled=True, required=True, label = self.label_2 )

        self.fields["group_prod"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["Группа продукции"], disabled=True, required=True, label = self.label_3)

        self.fields["error"] = forms.CharField(
            max_length=100, initial=str(self.result["Наличие ошибки"])[0], disabled=True, required=False)


class MapTwo(forms.Form):
    def __init__(self, result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = result

        self.fields["code"] = forms.CharField(
            max_length=100, initial="Продукция " + self.result["Код"], disabled=True, required=True)
        self.fields["common_naming"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["Общее наименование продукции"], disabled=True, required=True)
        self.fields["tn_ved"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["ТН ВЭД ЕАЭС"], disabled=True, required=True)
        self.fields["tech_req"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["Технические регламенты"], disabled=True, required=True)
        self.fields["group_prod"] = forms.CharField(widget=forms.Textarea(
        ), max_length=10000, initial=self.result["Группа продукции"], disabled=True, required=True)
