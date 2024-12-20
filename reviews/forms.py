from django import forms
from reviews.models import Reviews
from django.utils.html import strip_tags

from sewajual.models import Vehicle

class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ["title", 'vehicle', "rating", "description"]
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        mood = self.cleaned_data["title"]
        return strip_tags(mood)

    def clean_description(self):
        feelings = self.cleaned_data["description"]
        return strip_tags(feelings)