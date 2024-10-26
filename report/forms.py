from django.forms import ModelForm
from report.models import Report
from django.utils.html import strip_tags

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['vehicle', 'issue_type', 'description']  

    def clean_vehicle(self):
        vehicle = self.cleaned_data["vehicle"]
        return strip_tags(vehicle)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)

    def clean_issue_type(self):
        issue_type = self.cleaned_data["issue_type"]
        return strip_tags(issue_type)
