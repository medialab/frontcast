from django import forms

class OffsetLimitForm(forms.Form):
  offset = forms.IntegerField(min_value=0, required=False, initial=0)
  limit  = forms.IntegerField(min_value=1, max_value=100, required=False, initial=25)
