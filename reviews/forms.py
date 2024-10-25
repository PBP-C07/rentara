from django.forms import ModelForm
from reviews.models import Reviews

class ReviewsForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ["title", "rating", "description"]