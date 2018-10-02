from django.contrib.auth import forms
from smartdiabetes.models import User, InsulinRatio
from django import forms as forms2


class UserCreationForm2(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User

class ProfileForm(forms2.ModelForm):
    class Meta:
        model = User
        fields = ('address_city', 'address_street', 'address_no', 'sex')

class RatioForm(forms2.ModelForm):
    class Meta:
        model = InsulinRatio
        fields = ('insulin_ratio', 'start_time', 'end_time')
