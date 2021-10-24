from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.transaction import atomic
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import DateRangeForm
from .models import Category, Record


class IndexView(generic.CreateView):
    model = Record

    template_name = 'index.html'

    fields = ['date', 'category', 'sum']

    def get_context_data(self, **kwargs):
        kwargs['categories'] = list(
            Category.objects.order_by('priority').values('name').all()
        )

        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('expenses:submitted')


class HistoryView(LoginRequiredMixin, generic.ListView):
    model = Record

    template_name = 'history.html'

    ordering = ['-time']

    DEFAULT_COUNT = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        count = self.request.GET.get('count')

        if count is None or not count.isdigit():
            return queryset[:self.DEFAULT_COUNT]
        else:
            return queryset[:int(count)]


class RecordDetailView(LoginRequiredMixin, generic.UpdateView):
    model = Record

    fields = ['date', 'category', 'sum']

    template_name = 'record.html'

    def get_success_url(self):
        return reverse('expenses:record', args=[self.object.id])


def submitted(request):
    return render(request, 'submitted.html')


@login_required
@atomic
def stats(request):
    form = DateRangeForm(request.GET)

    if form.is_valid():
        begin = form.cleaned_data['begin_date']
        end = form.cleaned_data['end_date']

        records = Record.objects \
            .filter(date__lte=end, date__gte=begin) \
            .values('category') \
            .annotate(total=Sum('sum')) \
            .order_by('total') \
            .values_list('category', 'total', named=True)
    

        total = Record.objects \
            .filter(date__lte=end, date__gte=begin) \
            .aggregate(total=Sum('sum'))['total'] or 0
    else:
        records, total = (), 0
        form = DateRangeForm()

    return render(request, 'stats.html', context={
        'records': records,
        'total': total,
        'form': form,
    })
