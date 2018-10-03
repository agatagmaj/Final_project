from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from smartdiabetes.forms import UserCreationForm2, ProfileForm, RatioForm, SensitivityForm, TargetedLevelsForm, \
    InsulinActionForm, AddMenuForm, CalculateMealForm
from smartdiabetes.models import InsulinRatio, InsulinSensitivity, InsulinAction, TargetedLevels, User, Menu


class HomeView(View):
    # todo wywalić błąd jeżeli wprowadzanie danych jest nieskończone
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


class ProfileView(LoginRequiredMixin,View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Podstawowe informacje"})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('insulin-ratio')
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Podstawowe informacje"
                       })


class RatioView(LoginRequiredMixin, View):
    def get(self, request):
        if request.session.get('last_end_time'):
            new_start_time = request.session['last_end_time']
        else:
            new_start_time = 0
        form = RatioForm(initial={'start_time': new_start_time})
        return render(request, 'smartdiabetes/signup.html',
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
                if InsulinSensitivity.objects.filter(user = request.user).exists():
                    return redirect('home')
                else:
                    return redirect('insulin-sensitivity')
            else:
                request.session['last_end_time'] = form.cleaned_data['end_time']
                return redirect('insulin-ratio')
        return render(request, 'smartdiabetes/signup.html',
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
        return render(request, 'smartdiabetes/signup.html',
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
                if TargetedLevels.objects.filter(user = request.user).exists():
                    return redirect('home')
                else:
                    return redirect('target-level')
            else:
                request.session['sens_end_time'] = form.cleaned_data['end_time']
                return redirect('insulin-sensitivity')
        return render(request, 'smartdiabetes/signup.html',
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
        return render(request, 'smartdiabetes/signup.html',
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
                if InsulinAction.objects.filter(user = request.user).exists():
                    return redirect('home')
                else:
                    return redirect('insulin-action')
            else:
                request.session['targ_end_time'] = form.cleaned_data['end_time']
                return redirect('target-level')
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Poziom docelowy",
                       "help_text": 'Podaj zakres docelowy glikemii, '
                                    'wartość nie może być niższa niż 70 i wyższa niż 180',
                       })

class InsulinActionView(LoginRequiredMixin,View):
    def get(self, request):
        form = InsulinActionForm()
        return render(request, 'smartdiabetes/signup.html',
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
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Długość działania insuliny",
                       "help_text": 'Podaj długość działania w godzinach'
                       })

class UpdateRatioView(LoginRequiredMixin, View):
    def get(self, request):
        InsulinRatio.objects.filter(user = request.user).delete()
        request.session['last_end_time'] = 0
        return redirect('insulin-ratio')

class UpdateSensitivityView(LoginRequiredMixin, View):
    def get(self, request):
        InsulinSensitivity.objects.filter(user = request.user).delete()
        request.session['sens_end_time'] = 0
        return redirect('insulin-sensitivity')

class UpdateTargetedView(LoginRequiredMixin, View):
    def get(self, request):
        TargetedLevels.objects.filter(user = request.user).delete()
        request.session['targ_end_time'] = 0
        return redirect('target-level')

class UpdateInsulinActionView(LoginRequiredMixin, View):
    def get(self, request):
        InsulinAction.objects.filter(user=request.user).delete()
        return redirect('insulin-action')

class UpdateProfileView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'address_city', 'address_street', 'address_no', 'sex']
    template_name = 'smartdiabetes/signup.html'
    success_url = reverse_lazy('home')


    def get_object(self, queryset=None):
        return self.request.user

class AddMenuView(CreateView):
    form_class = AddMenuForm
    model = Menu
    success_url = reverse_lazy('menu')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

class MenuView(ListView):
    template_name = 'smartdiabetes/menu_food.html'
    context_object_name = 'menu'

    def get_queryset(self):
        return Menu.objects.filter(user = self.request.user)

class CalculateMealView(View):
    def get(self, request):
        form = CalculateMealForm()
        form.fields['meal'].queryset = Menu.objects.filter(user = request.user)
        return render(request, 'smartdiabetes/signup.html',
                      {"form": form,
                       "head": "Wyliczenie posiłku",
                       "help_text": 'Podaj ilość wymienników lub wybierz posiłek z listy'
                       })


