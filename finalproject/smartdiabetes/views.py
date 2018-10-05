import os
import time
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from pygal.style import Style

from smartdiabetes.forms import UserCreationForm2, ProfileForm, RatioForm, SensitivityForm, TargetedLevelsForm, \
    InsulinActionForm, AddMenuForm, CalculateMealForm, CalculateCorrectionForm, IfMealForm, AddGlucoseLevelForm
from smartdiabetes.models import InsulinRatio, InsulinSensitivity, InsulinAction, TargetedLevels, User, Menu, \
    BloodGlucoseResults, Meals, InsulinInjections
from pygal import Bar, DateTimeLine


class HomeView(View):
    # todo dodać zdjęcie do strony logowania / rejestracji
    # todo wywalić błąd jeżeli wprowadzanie danych jest nieskończone - on się wywala, ale trzeba się przed nim zabezpieczyć
    # czy istnieje jakikolwiek rekord kończący się na 24 w end_time
    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            ctx = {"msg": "Nie zalogowałeś się baranie!"}
            return redirect("signup")
        else:
            insulin_ration = InsulinRatio.objects.filter(user=request.user)
            insulin_sensitivity = InsulinSensitivity.objects.filter(user=request.user)
            insulin_action = InsulinAction.objects.get(user=request.user)
            targeted_levels = TargetedLevels.objects.filter(user=request.user)
            return render(request, 'smartdiabetes/user_home.html', locals())


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm2()
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Zarejestruj się"
                       })

    def post(self, request):
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Zarejestruj się"
                       })


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Podstawowe informacje"})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('insulin-ratio')
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Podstawowe informacje"
                       })


# todo założenie, że przelicznik dla ww i wbt jest taki sam - do poprawy
class RatioView(LoginRequiredMixin, View):
    def get(self, request):
        if request.session.get('last_end_time'):
            new_start_time = request.session['last_end_time']
        else:
            new_start_time = 0
        form = RatioForm(initial={'start_time': new_start_time})
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Przelicznik",
                       "help_text": 'Podaj ilość insuliny na jeden wymiennik'
                       })

    def post(self, request):
        if request.session.get('last_end_time'):
            new_start_time = request.session['last_end_time']
        else:
            new_start_time = 0
        form = RatioForm(request.POST, initial={'start_time': new_start_time})
        if form.is_valid():
            ratio = form.save(commit=False)
            ratio.user = request.user
            ratio.save()
            if form.cleaned_data['end_time'] == 24:
                if InsulinSensitivity.objects.filter(user=request.user).exists():
                    return redirect('home')
                else:
                    return redirect('insulin-sensitivity')
            else:
                request.session['last_end_time'] = form.cleaned_data['end_time']
                return redirect('insulin-ratio')
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Przelicznik",
                       "help_text": 'Podaj ilość insuliny na jeden WW'
                       })


class SensitivityView(LoginRequiredMixin, View):
    def get(self, request):
        if request.session.get('sens_end_time'):
            new_start_time = request.session['sens_end_time']
        else:
            new_start_time = 0
        form = SensitivityForm(initial={'start_time': new_start_time})
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Wrażliwość",
                       "help_text": 'Podaj wrażliwość na jednostkę insuliny'
                       })

    def post(self, request):
        if request.session.get('sens_end_time'):
            new_start_time = request.session['sens_end_time']
        else:
            new_start_time = 0
        form = SensitivityForm(request.POST, initial={'start_time': new_start_time})
        if form.is_valid():
            sensitivity = form.save(commit=False)
            sensitivity.user = request.user
            sensitivity.save()
            if form.cleaned_data['end_time'] == 24:
                if TargetedLevels.objects.filter(user=request.user).exists():
                    return redirect('home')
                else:
                    return redirect('target-level')
            else:
                request.session['sens_end_time'] = form.cleaned_data['end_time']
                return redirect('insulin-sensitivity')
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Wrażliwość",
                       "help_text": 'Podaj wrażliwość na jednostkę insuliny'
                       })


class TargetedView(LoginRequiredMixin, View):
    def get(self, request):
        if request.session.get('targ_end_time'):
            new_start_time = request.session['targ_end_time']
        else:
            new_start_time = 0
        form = TargetedLevelsForm(initial={'start_time': new_start_time})
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Poziom docelowy",
                       "help_text": 'Podaj zakres docelowy glikemii, '
                                    'wartość nie może być niższa niż 70 i wyższa niż 180',
                       })

    def post(self, request):
        if request.session.get('targ_end_time'):
            new_start_time = request.session['targ_end_time']
        else:
            new_start_time = 0
        form = TargetedLevelsForm(request.POST, initial={'start_time': new_start_time})
        if form.is_valid():
            sensitivity = form.save(commit=False)
            sensitivity.user = request.user
            sensitivity.save()
            if form.cleaned_data['end_time'] == 24:
                if InsulinAction.objects.filter(user=request.user).exists():
                    return redirect('home')
                else:
                    return redirect('insulin-action')
            else:
                request.session['targ_end_time'] = form.cleaned_data['end_time']
                return redirect('target-level')
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Poziom docelowy",
                       "help_text": 'Podaj zakres docelowy glikemii, '
                                    'wartość nie może być niższa niż 70 i wyższa niż 180',
                       })


class InsulinActionView(LoginRequiredMixin, View):
    def get(self, request):
        form = InsulinActionForm()
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Długość działania insuliny",
                       "help_text": 'Podaj długość działania w godzinach'
                       })

    def post(self, request):
        form = InsulinActionForm(request.POST)
        if form.is_valid():
            insulin_action = form.save(commit=False)
            insulin_action.user = request.user
            insulin_action.save()
            return redirect('home')
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Długość działania insuliny",
                       "help_text": 'Podaj długość działania w godzinach'
                       })


class UpdateRatioView(LoginRequiredMixin, View):
    def get(self, request):
        InsulinRatio.objects.filter(user=request.user).delete()
        request.session['last_end_time'] = 0
        return redirect('insulin-ratio')


class UpdateSensitivityView(LoginRequiredMixin, View):
    def get(self, request):
        InsulinSensitivity.objects.filter(user=request.user).delete()
        request.session['sens_end_time'] = 0
        return redirect('insulin-sensitivity')


class UpdateTargetedView(LoginRequiredMixin, View):
    def get(self, request):
        TargetedLevels.objects.filter(user=request.user).delete()
        request.session['targ_end_time'] = 0
        return redirect('target-level')


class UpdateInsulinActionView(LoginRequiredMixin, View):
    def get(self, request):
        InsulinAction.objects.filter(user=request.user).delete()
        return redirect('insulin-action')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'address_city', 'address_street', 'address_no', 'sex']
    template_name = 'smartdiabetes/form.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


class AddMenuView(LoginRequiredMixin, CreateView):
    form_class = AddMenuForm
    model = Menu
    success_url = reverse_lazy('menu')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class MenuView(LoginRequiredMixin, ListView):
    template_name = 'smartdiabetes/menu_food.html'
    context_object_name = 'menu'

    def get_queryset(self):
        return Menu.objects.filter(user=self.request.user)


# todo czy podano i jeśli tak to zapisać w wynikach
# todo info kiedy należy zmierzyć cukier
class CalculateMealView(LoginRequiredMixin, View):
    def get(self, request):
        form = CalculateMealForm()
        form.fields['meal'].queryset = Menu.objects.filter(user=request.user)
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Wyliczenie dawki",
                       "help_text": 'Podaj ilość wymienników lub wybierz posiłek z listy'
                       })

    def post(self, request):
        form = CalculateMealForm(request.POST)
        if form.is_valid():
            ww = form.cleaned_data['ww']
            wbt = form.cleaned_data['wbt']
            glycemia = form.cleaned_data['glycemia']
            os.environ['TZ'] = 'Poland'
            time.tzset()
            actual_hour = time.strftime("%H")
            insulin_ratio = InsulinRatio.objects.filter(user=request.user).filter(start_time__lte=actual_hour).filter(
                end_time__gt=actual_hour)
            insulin_sensitivity = InsulinSensitivity.objects.filter(user=request.user).filter(
                start_time__lte=actual_hour).filter(
                end_time__gt=actual_hour)
            insulin_sensitivity = insulin_sensitivity[0].insulin_sensitivity
            targeted_levels = TargetedLevels.objects.filter(user=request.user).filter(
                start_time__lte=actual_hour).filter(
                end_time__gt=actual_hour)
            min = targeted_levels[0].min_level
            max = targeted_levels[0].max_level
            optimal_level = (max + min) / 2
            insulin_for_ww = float(insulin_ratio[0].insulin_ratio) * ww
            insulin_for_wbt = float(insulin_ratio[0].insulin_ratio) * wbt
            time_for_wbt = insulin_for_wbt + 2
            if glycemia > max:
                insulin_for_correction = (glycemia - optimal_level) / insulin_sensitivity
                bolus = insulin_for_correction + insulin_for_ww
            else:
                bolus = insulin_for_ww
            # todo dodać zaokrąglanie do 0,5
            # todo zastanowić się jak uzwględnić insulin in action
            # insulin_action = InsulinAction.objects.get(user=request.user)
            request.session['glucose'] = glycemia
            request.session['ww'] = ww
            request.session['wbt'] = wbt
            # todo zmienić, bo ograniczenie że nie ma podziału na bolus pod, roz i korekte
            request.session['insulin_dose'] = bolus + insulin_for_wbt
            form = IfMealForm()
            return render(request, 'smartdiabetes/insulin.html', locals())
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Wyliczenie posiłku",
                       "help_text": 'Podaj ilość wymienników lub wybierz posiłek z listy'
                       })


class CalculateCorrectionView(LoginRequiredMixin, View):
    def get(self, request):
        form = CalculateCorrectionForm()
        return render(request, 'smartdiabetes/form.html',
                      {"form": form,
                       "head": "Wyliczenie korekty",
                       })

    def post(self, request):
        form = CalculateCorrectionForm(request.POST)
        if form.is_valid():
            glycemia = form.cleaned_data['glycemia']
            os.environ['TZ'] = 'Poland'
            time.tzset()
            actual_hour = time.strftime("%H")
            insulin_sensitivity = InsulinSensitivity.objects.filter(user=request.user).filter(
                start_time__lt=actual_hour).filter(
                end_time__gt=actual_hour)
            insulin_sensitivity = insulin_sensitivity[0].insulin_sensitivity
            targeted_levels = TargetedLevels.objects.filter(user=request.user).filter(
                start_time__lt=actual_hour).filter(
                end_time__gt=actual_hour)
            min = targeted_levels[0].min_level
            max = targeted_levels[0].max_level
            optimal_level = (max + min) / 2
            if glycemia > max:
                correction = glycemia - optimal_level
                correction = correction / insulin_sensitivity
                form = IfMealForm()
                ctx = {
                    "correction": correction,
                    "form": form,
                }
                request.session['glucose'] = glycemia
                # todo zmienić, bo ograniczenie że nie ma podziału na bolus pod, roz i korekte
                request.session['insulin_dose'] = correction
                return render(request, 'smartdiabetes/correction.html', ctx)
            elif glycemia < min:
                ctx = {"warning": "Masz za niski poziom cukru - Zjedz coś!"}
                return render(request, 'smartdiabetes/correction.html', ctx)
            else:
                ctx = {"msg": "Twój poziom cukru jest prawidłowy"}
                return render(request, 'smartdiabetes/correction.html', ctx)


class AddRecordView(LoginRequiredMixin, View):
    def post(self, request):
        form = IfMealForm(request.POST)
        if form.is_valid():
            if 'glucose' in request.session:
                glucose = request.session['glucose']
            glucose_result = BloodGlucoseResults.objects.create(user=request.user, glucose=glucose)
            insulin = form.cleaned_data['insulin']
            if insulin:
                if 'ww' in request.session and 'wbt' in request.session:
                    ww = request.session['ww']
                    wbt = request.session['wbt']
                    meal = Meals.objects.create(user=request.user, glucose=glucose_result, ww=ww, wbt=wbt)
                    del request.session['ww']
                    del request.session['wbt']
                if 'insulin_dose' in request.session:
                    insulin_dose = request.session['insulin_dose']
                    if 'meal' in locals():
                        InsulinInjections.objects.create(user=request.user, glucose=glucose_result, meal=meal,
                                                         correction=0,
                                                         insulin_dose=insulin_dose)
                    else:
                        InsulinInjections.objects.create(user=request.user, glucose=glucose_result, correction=1,
                                                             insulin_dose=insulin_dose)
                    return redirect("stat")
            else:
                if 'ww' in request.session and 'wbt' in request.session:
                    del request.session['ww']
                    del request.session['wbt']
        return redirect("home")


class AddGlucoseLevelView(LoginRequiredMixin, CreateView):
    form_class = AddGlucoseLevelForm
    model = BloodGlucoseResults
    template_name = 'smartdiabetes/form.html'
    success_url = reverse_lazy('stat')

    def get_context_data(self, **kwargs):
        ctx = super(AddGlucoseLevelView, self).get_context_data(**kwargs)
        ctx['head'] = "Podaj poziom cukru"
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class StatView(LoginRequiredMixin, View):
    def get(self, request):
        glucose = BloodGlucoseResults.objects.filter(user=request.user, time__lt=datetime.now(),
                                                     time__gte=(datetime.now() - timedelta(hours=24)))

        custom_style = Style(
            background='transparent',
            plot_background='transparent',
            foreground_subtle='#FFD200',
            opacity='.6',
            opacity_hover='.9',
            transition='400ms ease-in',
            colors=('#FFD200', '#5B5B5B'))

        chart = DateTimeLine(
            height=600,
            width=1000,
            explicit_size=True,
            style=custom_style,
            show_legend=False,
            x_value_formatter=lambda dt: dt.strftime("%H:%M")
        )

        chart.add("Poziom cukru", [(item.time, item.glucose) for item in glucose])

        rendered_chart = chart.render(unicode=True)
        ctx = {}
        print(rendered_chart)
        ctx['chart'] = rendered_chart.decode("utf-8")

        meals = Meals.objects.filter(user=request.user, time__lt=datetime.now(),
                                                     time__gte=(datetime.now() - timedelta(hours=24)))
        insulin_inj = InsulinInjections.objects.filter(user=request.user, time__lt=datetime.now(),
                                     time__gte=(datetime.now() - timedelta(hours=24)))
        ctx['meals']=meals
        ctx['insulin_inj'] = insulin_inj
        return render(request, 'smartdiabetes/stat.html', ctx)
