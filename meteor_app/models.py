from django.db import models


class MoonPhase(models.Model):
    date = models.DateField()
    illumination_percentage = models.FloatField()

    def __str__(self):
        return f"Moon Phase on {self.date}"


class Constellation(models.Model):
    name = models.CharField(max_length=100)
    min_latitude = models.FloatField()
    max_latitude = models.FloatField()

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()

    def __str__(self):
        return self.name


class MeteorShower(models.Model):
    name = models.CharField(max_length=100)
    radiant_constellation = models.ForeignKey(Constellation, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name



# Create your models here.
