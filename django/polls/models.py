from django.db import models
import json
import re
import sys
# Create your models here.


class UserActivity(models.Model):
    team_member = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    team_member_backup = models.CharField(max_length=100)
    assigned_projects = models.TextField()
    achievements = models.TextField()
    project_end_date = models.CharField(max_length=100)

    def build_report(self) -> dict:
        template = {"update_type": "personal_update",
                    "payload": ""}
        current_report = {"team_member": self.team_member,
                          "team": self.team,
                          "status": self.status,
                          "team_member_backup": self.team_member_backup,
                          "assigned_projects": "",
                          "achievements": "",
                          "project_end_date": self.project_end_date}
        assigned_projects = str(self.assigned_projects).splitlines()
        buffer = str(self.achievements).split("]")
        achievements = dict()
        for i, project in enumerate(assigned_projects):
            buffer[i] += "]"
            str_project = "[" + project + "-"
            achievements[project] = buffer[i][buffer[i].find(
                str_project) + len(str_project):buffer[i].find("]")]
        current_report["assigned_projects"] = list(achievements.keys())
        current_report["achievements"] = list(achievements.items())
        template["payload"] = current_report
        return template
'''
    def invoke_lambda(self, report: dict) -> None:
        # with open("event_projects.json", 'w', encoding='utf-8') as f:
        #    json.dump(report, f, ensure_ascii=False, indent=4)
        # return 0

        lambda_func = boto3.client("lambda", region_name='us-east-1')
        try:
            response = lambda_func.invoke(
                FunctionName="arn:aws:lambda:us-east-1:409227834581:function:dataops-wrautomation-xlsx-converter",
                InvocationType="RequestResponse",  # Event
                Payload=json.dumps(report, ensure_ascii=False, indent=4)
            )

        except Exception as e:
            sys.stdout.write(str(e))
'''

class ProjectActivity(models.Model):
    team_member = models.CharField(max_length=100)
    project = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    last_week_achievements = models.TextField()
    last_project_updates = models.TextField()
    next_week_achievements = models.TextField()
    next_project_updates = models.TextField()

    def build_report(self) -> dict:
        template = {"update_type": "projects_update",
                    "payload": ""}
        current_report = {"team_member": self.team_member,
                          "projects": list()
                          }
        projects_template = {"project_name": "",
                             "last_week_achievements": "",
                             "next_week_achievements": "",
                             "project_updates": ""}
        data = list()

        if self.project == "Other":
            projects_template["project_name"] = self.project_name
        else:
            projects_template["project_name"] = self.project
        projects_template["last_week_achievements"] = str(
            self.last_week_achievements)[1:-1]
        projects_template["next_week_achievements"] = str(
            self.next_week_achievements)[1:-1]

        buffer = str(self.last_project_updates).split("]")
        buffer = list(filter(None, buffer))
        last_data = self.get_data(buffer)
        size_last = len(buffer)
        print(last_data)
        buffer = str(self.next_project_updates).split("]")
        buffer = list(filter(None, buffer))
        next_data = self.get_data(buffer)
        size_next = len(buffer)
        print(next_data)

        if size_last == size_next:
            for i in range(size_last):
                project_updates = {"ticket_number": "",
                                   "was_done": "",
                                   "future_ticket_number": "",
                                   "will_be_done": ""}
                project_updates["ticket_number"] = last_data["tickets"][i]
                project_updates["was_done"] = last_data["actions"][i]
                project_updates["future_ticket_number"] = next_data["tickets"][i]
                project_updates["will_be_done"] = next_data["actions"][i]
                data.append(project_updates)
        elif size_next < size_last:
            for i in range(size_last):
                project_updates = {"ticket_number": "",
                                   "was_done": "",
                                   "future_ticket_number": "",
                                   "will_be_done": ""}
                project_updates["ticket_number"] = last_data["tickets"][i]
                project_updates["was_done"] = last_data["actions"][i]
                if i < size_next:
                    project_updates["future_ticket_number"] = next_data["tickets"][i]
                    project_updates["will_be_done"] = next_data["actions"][i]
                data.append(project_updates)
        else:
            for i in range(size_next):
                project_updates = {"ticket_number": "",
                                   "was_done": "",
                                   "future_ticket_number": "",
                                   "will_be_done": ""}
                if i < size_last:
                    project_updates["ticket_number"] = last_data["tickets"][i]
                    project_updates["was_done"] = last_data["actions"][i]
                project_updates["future_ticket_number"] = next_data["tickets"][i]
                project_updates["will_be_done"] = next_data["actions"][i]
                data.append(project_updates)

        projects_template["project_updates"] = data
        current_report["projects"].append(projects_template)
        template["payload"] = current_report
        return template

    @staticmethod
    def get_data(buffer: list) -> dict:
        tickets, actions = list(), list()
        for i, v in enumerate(buffer):
            indexes = [m.start() for m in re.finditer('-', v)]
            tickets.append(v[v.find("[") + 1:indexes[1]])
            actions.append(v[indexes[1] + 1:])
        return {"tickets": tickets,
                "actions": actions}
