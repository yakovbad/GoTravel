from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from representation.models import UserProfile


class MyUserCreationForm(ModelForm):

    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = user.email
        user.is_staff = True
        if commit:
            user.save()
        return user
