from django import forms


class DateRangeForm(forms.Form):
    begin_date = forms.DateField(required=True)

    end_date = forms.DateField(required=True)
