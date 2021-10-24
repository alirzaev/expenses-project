from django.db import models


class Record(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    date = models.DateField()

    category = models.CharField(max_length=30)

    sum = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%y')}: {self.category}, {self.sum} р."


class Category(models.Model):
    name = models.CharField(max_length=30)

    priority = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.priority})'
