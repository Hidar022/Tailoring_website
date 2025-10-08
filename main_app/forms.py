from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'phone', 'address', 'gender', 'date_of_birth',
            'body_type', 'favorite_style', 'bio', 'profile_picture'
        ]
