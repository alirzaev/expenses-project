import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.transaction import atomic
from django.shortcuts import render, redirect

from .models import Record, Category


def index(request):
    categories = [category.name for category in Category.objects.order_by('priority').all()]
    return render(request, 'index.html', context={
        'categories': categories
    })


def submit(request):
    data = request.POST
    date = datetime.date.fromisoformat(data['date'])
    category = data['category']
    sum_ = data['sum'].replace(',', '.')
    if 'otherCategory' in data:
        category = data['otherCategory']

    record = Record(date=date, category=category, sum=sum_)
    record.save()

    return redirect('expenses:submitted')


def submitted(request):
    return render(request, 'submitted.html')


@login_required
def history(request):
    records = [(item.date.strftime('%d.%m.%y'),
                item.category,
                item.sum,
                item.time.strftime('%d.%m.%y %H:%M %z')) for item in
               Record.objects.order_by('-time').all()[:5]]

    return render(request, 'history.html', context={
        'records': records
    })


@login_required
@atomic
def stats(request):
    data = request.GET
    if 'begin' in data and 'end' in data:
        begin = datetime.date.fromisoformat(data['begin'])
        end = datetime.date.fromisoformat(data['end'])

        records = Record.objects\
            .filter(date__lte=end, date__gte=begin)\
            .values_list('category', named=True)\
            .annotate(s=Sum('sum'))\
            .order_by('s')

        total = Record.objects\
            .filter(date__lte=end, date__gte=begin)\
            .aggregate(total=Sum('sum'))['total'] or 0
    else:
        records, total = (), 0

    return render(request, 'stats.html', context={
        'records': records,
        'total': total
    })
