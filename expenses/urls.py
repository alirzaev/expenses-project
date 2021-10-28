from django.urls import path

from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('stats/', views.stats, name='stats'),
    path('submitted/', views.SubmittedView.as_view(), name='submitted'),
    path('record/<int:pk>/', views.RecordDetailView.as_view(), name='record'),
]
