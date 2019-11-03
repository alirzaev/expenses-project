from django.urls import path

from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('submitted', views.submitted, name='submitted'),
    path('history', views.history, name='history'),
    path('stats', views.stats, name='stats')
]
