from django.db import models


class Manufacture(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Model(models.Model):
    manufacture = models.ForeignKey(Manufacture, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    transmission = models.CharField(max_length=50)
    gear = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Parking(models.Model):
    presence = models.BooleanField(default=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    state_number = models.CharField(max_length=50)
    engine = models.BooleanField(default=False)
    open_doors = models.BooleanField(default=False)
