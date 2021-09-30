from django import forms
from .models import Image
from accounts.models import Settings

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img_file', 'description',)
        labels = {'img_file': 'Your image ', 'description': 'Description '}

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('is_public', 'show_slideshow')
        labels = {'is_public': 'Account visible to other users', 'show_slideshow': 'Enable slideshow on main gallery page'}