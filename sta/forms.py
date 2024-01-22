from django import forms
from .models import ImageUpload

class UserImageForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(UserImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
