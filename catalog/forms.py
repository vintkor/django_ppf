from django import forms
from .models import Order
from django.utils.translation import ugettext_lazy as _


class OrderForm(forms.ModelForm):
    phone = forms.CharField(label=_('Phone'), widget=forms.TextInput(
        attrs={'class': 'form-control product-detail__form__input', 'placeholder': '+38 (000) 000-00-00'},
    ))

    class Meta:
        model = Order
        fields = ('phone',)
