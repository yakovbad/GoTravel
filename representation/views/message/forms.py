from django.forms import ModelForm
from representation.models import Message


class SendMessage(ModelForm):
    class Meta:
        model = Message
        fields = ['text']
