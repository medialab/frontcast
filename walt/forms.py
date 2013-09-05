from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from walt.models import Document

class LoginForm(forms.Form):
	username = forms.CharField( label=_('login'), max_length=64 )
	password = forms.CharField( label=_('password'),  max_length=64, widget=forms.PasswordInput(render_value=False ) )

class DocumentForm(ModelForm):

  def clean(self):
    cleaned_data = super(DocumentForm, self).clean()

    type        = cleaned_data.get("type")
    reference   = cleaned_data.get("reference")
    status      = cleaned_data.get("status")

    cleaned_data['status'] = status if status != Document.PUBLIC else Document.WAITING_FOR_PUBLICATION

    if type == Document.REFERENCE_CONTROVERSY and len(reference)<24: # reference UNIQUEID
      self._errors['reference'] = self.error_class(["reference uuid is not valid"])
      del cleaned_data["reference"]

    return cleaned_data

  class Meta:
    model = Document
    exclude = ['owner']
