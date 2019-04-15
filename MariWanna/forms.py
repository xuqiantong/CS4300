from django import forms

class SearchForm(forms.Form):
    TOLERANCE_CHOICES = (
        ('N', 'No Tolerance'),
        ('L', 'Low Tolerance'),
        ('M', 'Mild Tolerance'),
        ('H', 'High Tolerance')
    )
    conditions = forms.CharField(max_length=250)
    undesired_effects = forms.CharField(max_length=250)
    # tolerance = forms.CharField(max_length=1, choices=TOLERANCE_CHOICES)
    age = forms.IntegerField()
    height = forms.IntegerField()
    weight = forms.IntegerField()