from django.contrib import admin
from import_export.admin import ExportActionMixin
from import_export.resources import ModelResource
from rangefilter.filter import DateRangeFilter

from .models import Record, Category


class RecordResource(ModelResource):
    class Meta:
        model = Record

        fields = ('date', 'category', 'sum')

        widgets = {
            'date': {
                'format': '%d.%m.%Y'
            }
        }


class RecordAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = RecordResource

    list_filter = (('date', DateRangeFilter),)

    ordering = ('-date', '-time')

    readonly_fields = ('time',)


class CategoryResource(ModelResource):
    class Meta:
        model = Category

        fields = ('name', 'priority')


class CategoryAdmin(admin.ModelAdmin):
    resource_class = CategoryResource

    ordering = ('priority', 'name')


admin.site.register(Record, RecordAdmin)
admin.site.register(Category, CategoryAdmin)
