from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from smartdiabetes.forms import UserCreationForm2, ProfileForm, RatioForm
from smartdiabetes.models import InsulinRatio


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm2()
        return render(request, 'smartdiabetes/signup.html', {"form": form})

    def post(self, request):
        form = UserCreationForm2(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

class ProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'smartdiabetes/signup.html', {"form": form})

    def post(self, request):
        form = ProfileForm(request.POST)
        form.save()
        return redirect('insulin-ratio')

class RatioView(View):
    def get(self, request):
        if request.session.get('last_end_time'):
            new_start_time = request.session['last_end_time']
        else:
            new_start_time = 0
        form = RatioForm(initial={'start_time': new_start_time})
        return render(request, 'smartdiabetes/signup.html', {"form": form})

    def post(self, request):
        form = RatioForm(request.POST)
        ratio = form.save(commit=False)
        ratio.user = request.user
        ratio.save()
        if form.cleaned_data['end_time'] == 24:
            return HttpResponse("Dodałeś przelicznik")
        else:
            request.session['last_end_time'] = form.cleaned_data['end_time']
            return redirect('insulin-ratio')

    # todo disabled pole z zakresem czasu i ograniczenie czasu od 0 do 24