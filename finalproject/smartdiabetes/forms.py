from django.contrib.auth import forms
from django.utils.translation import gettext_lazy

from smartdiabetes.models import User, InsulinRatio, InsulinSensitivity, TargetedLevels, InsulinAction, Menu, \
    BloodGlucoseResults
from django import forms as forms2


class UserCreationForm2(forms.UserCreationForm):
    # password1 = forms2.CharField(
    #     label=gettext_lazy("Password"),
    #     strip=False,
    #     widget=forms2.PasswordInput,
    #     help_text="ekgfewkgfwh",
    # )

    # "Twoje hasło nie może być zbyt podobne do twoich innych danych osobistych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Twoje hasło nie może być powszechnie używanym hasłem.</li><li>Twoje hasło nie może składać się tylko z cyfr.</li></ul>" > < input

    class Meta(forms.UserCreationForm.Meta):
        model = User


class ProfileForm(forms2.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'address_city', 'address_street', 'address_no', 'sex')


# todo dodać ograniczenie z jakiego przedziału może być ratio i sensitivity
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

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if end_time > start_time:
            return cleaned_data
        else:
            raise forms2.ValidationError("Koniec zakresu nie może być mniejszy niż początek, popraw się")


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

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if end_time > start_time:
            return cleaned_data
        else:
            raise forms2.ValidationError("Koniec zakresu nie może być mniejszy niż początek, popraw się")


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

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if end_time > start_time:
            return cleaned_data
        else:
            raise forms2.ValidationError("Koniec zakresu nie może być mniejszy niż początek, popraw się")


class InsulinActionForm(forms2.ModelForm):
    class Meta:
        model = InsulinAction
        fields = ('insulin_in_action',)


class AddMenuForm(forms2.ModelForm):
    # todo ograniczyć, że gramy i wymienniki nie mogą być ujemne

    class Meta:
        model = Menu
        fields = ('name', 'carbo_grams', 'protein_grams', 'fat_grams', 'ww', 'wbt')

    def clean(self):
        cleaned_data = super().clean()
        carb = cleaned_data.get("carbo_grams")
        protein = cleaned_data.get("protein_grams")
        fat = cleaned_data.get("fat_grams")
        ww = cleaned_data.get("ww")
        wbt = cleaned_data.get("wbt")

        if ww is not None and wbt is not None:
            return cleaned_data
        else:
            if carb is not None and protein is not None and fat is not None:
                ww = carb / 10
                wbt = (fat * 9 + protein * 4) / 100
                cleaned_data['ww'] = ww
                cleaned_data['wbt'] = wbt
                return cleaned_data
            raise forms2.ValidationError("Nie podano wymaganych wartości")


class CalculateMealForm(forms2.Form):
    glycemia = forms2.IntegerField(min_value=0, label="Podaj poziom cukru")
    meal = forms2.ModelChoiceField(Menu.objects.all(), label="Posiłek", required=False)
    ww = forms2.FloatField(min_value=0, label="WW", required=False)
    wbt = forms2.FloatField(min_value=0, label="WBT", required=False)

    def clean(self):
        cleaned_data = super().clean()
        meal = cleaned_data.get("meal")
        ww = cleaned_data.get("ww")
        wbt = cleaned_data.get("wbt")

        if ww is not None and wbt is not None:
            return cleaned_data
        else:
            if meal:
                ww = meal.ww
                wbt = meal.wbt
                cleaned_data['ww'] = ww
                cleaned_data['wbt'] = wbt
                return cleaned_data
            raise forms2.ValidationError("Nie podano wymaganych wartości")


class CalculateCorrectionForm(forms2.Form):
    glycemia = forms2.IntegerField(min_value=0, label="Podaj poziom cukru")


class IfMealForm(forms2.Form):
    insulin = forms2.BooleanField(required=False, label="Czy podałeś insulinę?")


class AddGlucoseLevelForm(forms2.ModelForm):
    class Meta:
        model = BloodGlucoseResults
        fields = ('glucose',)

    def clean_glucose(self):
        data = self.cleaned_data['glucose']
        if data < 0:
            raise forms2.ValidationError("Podany poziom cukru jest nieprawidłowy, nie może być mniejszy od 0!")
        return data
