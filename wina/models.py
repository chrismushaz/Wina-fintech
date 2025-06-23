from django.db import models

# Create your models here.
class Institution(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    revenue = models.FloatField()
    def __str__(self):
        return self.name


class Booth(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    services = models.ManyToManyField(Institution, related_name="booths")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE)
    amount = models.IntegerField()
    service = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.booth.name + " - " + str(self.amount)
