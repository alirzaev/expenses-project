from django.db import models


class Record(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    date = models.DateField()

    category = models.CharField(max_length=30)

    sum = models.DecimalField(max_digits=9, decimal_places=2)

    def __repr__(self):
        return 'Record(time=%s, date=%s, category=%s, sum=%s)' % (
            self.time, self.date, self.category, self.sum)

    def __str__(self):
        return f"{self.date.strftime('%d.%m.%y')}: {self.category}, {self.sum} р."


class Category(models.Model):

    name = models.CharField(max_length=30)

    priority = models.IntegerField(default=0)

    def __repr__(self):
        return 'Category(name=%s, priority=%s)' % (
            self.name, self.priority
        )

    def __str__(self):
        return f'{self.name} ({self.priority})'
