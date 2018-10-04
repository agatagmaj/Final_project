from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

SEX_CHOICES = {
    (0, "niezdefiniowana"),
    (1, "mężczyzna"),
    (2, "kobieta")
}


class User(AbstractUser):
    address_city = models.CharField(max_length=64, verbose_name="Miasto")
    address_street = models.CharField(max_length=64, verbose_name="Ulica")
    address_no = models.CharField(max_length=64, verbose_name="Numer domu")
    sex = models.IntegerField(choices=SEX_CHOICES, default=0, verbose_name="Płeć")
    # todo for BMI calculation
    # height = models.DecimalField(max_digits=5, decimal_places=2)
    # weight = models.DecimalField(max_digits=5, decimal_places=2)
    # todo dodać zdjęcie
    # photo = models.ImageField(verbose_name="Zdjęcie")


class InsulinRatio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insulin_ratio = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Przelicznik")
    start_time = models.IntegerField(verbose_name="Zakres czasu od")
    end_time = models.IntegerField(verbose_name="Zakres czasu do")


class InsulinSensitivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insulin_sensitivity = models.IntegerField(verbose_name="Wrażliwość na insulinę")
    start_time = models.IntegerField(verbose_name="Zakres czasu od")
    end_time = models.IntegerField(verbose_name="Zakres czasu do")


class InsulinAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insulin_in_action = models.IntegerField(verbose_name="Czas działania insuliny")


class TargetedLevels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_level = models.IntegerField(verbose_name="Zakres docelowy od")
    max_level = models.IntegerField(verbose_name="Zakres docelowy do")
    start_time = models.IntegerField()
    end_time = models.IntegerField(verbose_name="Zakres czasu do")


class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nazwa posiłku")
    carbo_grams = models.IntegerField(verbose_name="Ile gram węglowodanów", blank=True, null=True)
    protein_grams = models.IntegerField(verbose_name="Ile gram białka", blank=True, null=True)
    fat_grams = models.IntegerField(verbose_name="Ile gram tłuszczy", blank=True, null=True)
    ww = models.FloatField(blank=True, verbose_name="WW")
    wbt = models.FloatField(blank=True, verbose_name="WBT")

    def __str__(self):
        return f"{self.name}"


class TemporaryMenu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nazwa posiłku")
    carbo_grams = models.IntegerField(verbose_name="Ile gram węglowodanów", blank=True, null=True)
    protein_grams = models.IntegerField(verbose_name="Ile gram białka", blank=True, null=True)
    fat_grams = models.IntegerField(verbose_name="Ile gram tłuszczy", blank=True, null=True)
    ww = models.FloatField(blank=True, verbose_name="WW")
    wbt = models.FloatField(blank=True, verbose_name="WBT")


class BloodGlucoseResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    glucose = models.IntegerField(verbose_name="Podaj glikemie")
    time = models.DateTimeField(auto_now_add=True)


class Meals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    glucose = models.ForeignKey(BloodGlucoseResults, on_delete=models.CASCADE)
    ww = models.FloatField(blank=True, verbose_name="WW")
    wbt = models.FloatField(blank=True, verbose_name="WBT")
    time = models.DateTimeField(auto_now_add=True)


class InsulinInjections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    glucose = models.ForeignKey(BloodGlucoseResults, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meals, on_delete=models.CASCADE, blank=True, null=True)
    correction = models.BooleanField(default=0)
    insulin_dose = models.FloatField(verbose_name="Dawka insuliny")
    time = models.DateTimeField(auto_now_add=True)
