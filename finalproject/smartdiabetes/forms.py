from django.contrib.auth import forms
from smartdiabetes.models import User, InsulinRatio, InsulinSensitivity, TargetedLevels, InsulinAction, Menu
from django import forms as forms2


class UserCreationForm2(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User

class ProfileForm(forms2.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'address_city', 'address_street', 'address_no', 'sex')

#todo dodać ograniczenie z jakiego przedziału może być ratio i sensitivity
class RatioForm(forms2.ModelForm):
    start_time = forms2.IntegerField(disabled=True, label="Zakres czasu od")

    class Meta:
        model = InsulinRatio
        fields = ('insulin_ratio', 'start_time', 'end_time')

    def clean_end_time(self):
        data = self.cleaned_data['end_time']
        if data > 24:
            raise forms2.ValidationError("Podany zakres czasu jest nieprawidłowy, doba ma tylko 24h!")
        return data

class SensitivityForm(forms2.ModelForm):
    start_time = forms2.IntegerField(disabled=True, label="Zakres czasu od")

    class Meta:
        model = InsulinSensitivity
        fields = ('insulin_sensitivity', 'start_time', 'end_time')

    def clean_end_time(self):
        data = self.cleaned_data['end_time']
        if data > 24:
            raise forms2.ValidationError("Podany zakres czasu jest nieprawidłowy, doba ma tylko 24h!")
        return data

class TargetedLevelsForm(forms2.ModelForm):
    start_time = forms2.IntegerField(disabled=True, label="Zakres czasu od")

    class Meta:
        model = TargetedLevels
        fields = ('min_level', 'max_level', 'start_time', 'end_time')

    def clean_end_time(self):
        data = self.cleaned_data['end_time']
        if data > 24:
            raise forms2.ValidationError("Podany zakres czasu jest nieprawidłowy, doba ma tylko 24h!")
        return data

    def clean_min_level(self):
        data = self.cleaned_data['min_level']
        if data < 70:
            raise forms2.ValidationError("Podano zbyt niski zakres docelowy glikemii")
        return data

    def clean_max_level(self):
        data = self.cleaned_data['max_level']
        if data > 180:
            raise forms2.ValidationError("Podano zbyt wysoki zakres docelowy glikemii")
        return data

class InsulinActionForm(forms2.ModelForm):

    class Meta:
        model = InsulinAction
        fields = ('insulin_in_action',)

class AddMenuForm(forms2.ModelForm):
    #todo ograniczyć, że gramy i wymienniki nie mogą być ujemne

    class Meta:
        model = Menu
        fields = ('name', 'carbo_grams', 'protein_grams', 'fat_grams', 'ww', 'wbt' )

    def clean(self):
        cleaned_data = super().clean()
        carb = cleaned_data.get("carbo_grams")
        protein = cleaned_data.get("protein_grams")
        fat = cleaned_data.get("fat_grams")
        ww = cleaned_data.get("ww")
        wbt = cleaned_data.get("wbt")

        if ww and wbt:
            return cleaned_data
        else:
            if carb and protein and fat:
                ww = carb / 10
                wbt = (fat * 9 + protein * 4)/100
                cleaned_data['ww'] = ww
                cleaned_data['wbt'] = wbt
                return cleaned_data
            raise forms2.ValidationError("Nie podano wymaganych wartości")

class CalculateMealForm(forms2.Form):
    meal = forms2.ModelChoiceField(Menu.objects.all(), label = "Posiłek", required=False)
    ww = forms2.FloatField(min_value=0, label="WW", required=False)
    wbt = forms2.FloatField(min_value=0, label="WBT", required=False)
