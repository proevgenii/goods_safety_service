from django import forms
from django.core import validators
from collections import deque

TEAM_MEMBERS = (("Yakimenko, Alexey", "Yakimenko, Alexey"),
                ("Hernandez, Hector", "Hernandez, Hector"),
                ("Karasev, Aleksei", "Karasev, Aleksei"),
                ("Muratov, Simar", "Muratov, Simar"),
                ("Lukashin, Alexey", "Lukashin, Alexey"),
                ("CastroMeza, Jesus", "CastroMeza, Jesus"),
                ("Millan, Sebastian", "Millan, Sebastian"))

BACKUP_MEMBERS = (("Lukashin, Alexey", "Lukashin, Alexey"),
                  ("Yakimenko, Alexey", "Yakimenko, Alexey"),
                  ("Millan, Sebastian", "Millan, Sebastian"),
                  ("CastroMeza, Jesus", "CastroMeza, Jesus"),
                  ("Muratov, Simar", "Muratov, Simar"),
                  ("Hernandez, Hector", "Hernandez, Hector"),
                  ("Karasev, Aleksei", "Karasev, Aleksei"))

PROJECT_END_DATE = (("Development Support", "Development\nSupport"),
                    ("KOP: Operational Support", "KOP: Operational\nSupport"),
                    ("ITO: Development Support", "ITO: Development\nSupport"),
                    ("ITO: Development Support KOP: Operational Support", "ITO: Development\nSupport\nKOP: Operational\nSupport"))


EXAMPLES = (("DataOps\nOneID SSO\nPOC's"),
            ("[DataOps-developed the first component of auto-reporter, ready to deploy]\n[OneID SSO-made all necessary changes in OpAMs]\n[POC's-wrote a code example\
           of transfering data from Athena to PowerBi through AWS tools]"),
            ("[SEA-4506-implemented approval processes and email notifications in ROM's intake process (assignment about implementation is for the review process)]\n[SEA-4509-added test mode\
                 to frontend to automatically fill up the forms by calling a lambda function with predefined answers]"),
            ("[SEA-4506-will merge if there are no problems in the associated pull request]\n[SEA-4509-will make script to upload frontend to repository to Confluence]"),
            ("Name of other project (enter if not selected in previous point)"),
            ("[Worked on the new types of inventory files. Fixed issues with data gathering from Jira]"),
            ("[Will work on incorporating new OpsRamp data dictionary]"))

PROJECTS = (("KOP", "KOP"),
            ("ITO", "ITO"),
            ("GBS - DXG AutoOnboarding Process",
             "GBS - DXG AutoOnboarding Process"),
            ("Team Analytics and Performance", "Team Analytics and Performance"),
            ("BCD Documentation and OpAMs", "BCD Documentation and OpAMs"),
            ("Other", "Other"))


def check_project(value: list) -> None:
    data = str(value).splitlines()
    deque(map(lambda x: x.lower(), data))
    if "opam" in data or "bcd" in data:
        raise forms.ValidationError("OpAM/BCD is not a project")


def check_quantity(projects: list, achievements: list) -> bool:
    return len(str(projects).splitlines()) == len(str(achievements).splitlines())


def check_brackets(value: list) -> None:
    data = str(value).splitlines()
    for line in data:
        if "[" not in line or "]" not in line:
            raise forms.ValidationError(
                "You should use '[' and ']' for every achievement or update")


def check_dashes(value: list) -> None:
    data = str(value).splitlines()
    for line in data:
        if line.count("-") < 2:
            raise forms.ValidationError(
                "You should enter data like 'ticket-number-update' for every update")


class UserForm(forms.Form):

    team_member = forms.ChoiceField(choices=TEAM_MEMBERS)
    team = forms.CharField(max_length=100, initial="Solutions Design")
    status = forms.CharField(max_length=100, initial="Active")
    team_member_backup = forms.ChoiceField(choices=BACKUP_MEMBERS)
    assigned_projects = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[0]}), max_length=300, help_text=EXAMPLES[0], validators=[check_project, ])
    achievements = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[1]}), max_length=300, help_text=EXAMPLES[1],)
    project_end_date = forms.ChoiceField(choices=PROJECT_END_DATE)

    def clean_achievements(self):
        cleaned_data = super(UserForm, self).clean()
        projects = cleaned_data.get('assigned_projects')
        achievements = cleaned_data.get('achievements')
        if not check_quantity(projects,   achievements):
            raise forms.ValidationError(
                "Quantity of projects must be the same in both projects' and achievements' fields")
        for line in str(achievements).splitlines():
            if "[" not in line or "]" not in line:
                raise forms.ValidationError(
                    "You should use '[' and ']' for every achievement")
        return cleaned_data.get('achievements')


class ProjectForm(forms.Form):

    team_member = forms.ChoiceField(choices=TEAM_MEMBERS)
    project = forms.ChoiceField(choices=PROJECTS)
    project_name = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[4]}), max_length=300, help_text=EXAMPLES[4], required=False)
    last_week_achievements = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[5]}), max_length=300, help_text=EXAMPLES[5], validators=[check_brackets, ])
    last_project_updates = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[2]}), max_length=300, help_text=EXAMPLES[2], validators=[check_brackets, check_dashes, ])
    next_week_achievements = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[6]}), max_length=300, help_text=EXAMPLES[6], validators=[check_brackets, ])
    next_project_updates = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': EXAMPLES[3]}), max_length=300, help_text=EXAMPLES[3], validators=[check_brackets, check_dashes, ])
