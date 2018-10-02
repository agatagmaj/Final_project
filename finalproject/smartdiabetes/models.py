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
    insulin_sensitivity = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()

class TargetedLevels(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insulin_in_action = models.IntegerField()
    min_level = models.IntegerField()
    max_level = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()

class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    carbo_grams = models.IntegerField(null=True, blank=True)
    protein_grams = models.IntegerField(null=True, blank=True)
    fat_grams = models.IntegerField(null=True, blank=True)
    ww = models.DecimalField(max_digits=4, decimal_places=2)
    wbt = models.DecimalField(max_digits=4, decimal_places=2)

class TemporaryMenu(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    carbo_grams = models.IntegerField()
    protein_grams = models.IntegerField()
    fat_grams = models.IntegerField()
    ww = models.DecimalField(max_digits=4, decimal_places=2)
    wbt = models.DecimalField(max_digits=4, decimal_places=2)

class InsulinResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    insulin_level = models.IntegerField()
    time = models.IntegerField()
