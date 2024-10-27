from django.forms import ModelForm
from reviews.models import Reviews
from django.utils.html import strip_tags

class ReviewsForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ["title", "rating", "description"]

    def clean_title(self):
        mood = self.cleaned_data["title"]
        return strip_tags(mood)

    def clean_description(self):
        feelings = self.cleaned_data["description"]
        return strip_tags(feelings)