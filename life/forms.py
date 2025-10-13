from django import forms

class DateConversionForm(forms.Form):
    gregorian_date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'date',
        'placeholder': 'Select a date',
    }))
