from django.db import models


class Resident(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class House(models.Model):
    address = models.CharField(max_length=200)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)

    def __str__(self):
        return self.address


class MaintenanceRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)

    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
