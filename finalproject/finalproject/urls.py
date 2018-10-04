"""finalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from smartdiabetes.views import SignUpView, ProfileView, RatioView, HomeView, SensitivityView, TargetedView, \
    InsulinActionView, UpdateRatioView, UpdateSensitivityView, UpdateTargetedView, UpdateInsulinActionView, \
    UpdateProfileView, AddMenuView, MenuView, CalculateMealView, CalculateCorrectionView, AddRecordView, \
    AddGlucoseLevelView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^profile$', ProfileView.as_view(), name='profile'),
    url(r'^profile/ratio$', RatioView.as_view(), name='insulin-ratio'),
    url(r'^profile/ratio/sensitivity$', SensitivityView.as_view(), name='insulin-sensitivity'),
    url(r'^profile/ratio/sensitivity/target_levels$', TargetedView.as_view(), name='target-level'),
    url(r'^profile/ratio/sensitivity/target_levels/action$', InsulinActionView.as_view(), name='insulin-action'),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^update/ratio$', UpdateRatioView.as_view(), name='update-ratio'),
    url(r'^update/sensitivity$', UpdateSensitivityView.as_view(), name='update-sensitivity'),
    url(r'^update/targets$', UpdateTargetedView.as_view(), name='update-targets'),
    url(r'^update/action$', UpdateInsulinActionView.as_view(), name='update-action'),
    url(r'^update/profile$', UpdateProfileView.as_view(), name='update-profile'),
    url(r'^add_menu$', AddMenuView.as_view(), name='add-menu'),
    url(r'^menu$', MenuView.as_view(), name='menu'),
    url(r'^calculate_meal$', CalculateMealView.as_view(), name='calculate-meal'),
    url(r'^calculate_correction$', CalculateCorrectionView.as_view(), name='calculate-correction'),
    url(r'^add_meal_record$', AddRecordView.as_view(), name='meal-record'),
    url(r'^add_glucose$', AddGlucoseLevelView.as_view(), name='add-glucose'),

]
