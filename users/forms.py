from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import CustomUser


class CreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'username', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']
