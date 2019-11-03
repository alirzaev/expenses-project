# Generated by Django 2.1 on 2019-03-28 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=30)),
                ('sum', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
    ]
