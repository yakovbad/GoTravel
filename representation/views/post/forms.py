from django.core.exceptions import ValidationError
from django.forms import ModelForm

from representation.models import Post


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text', "")
        if not text:
            raise ValidationError("Text must be not empty")
        return text
