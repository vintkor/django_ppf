from django import forms
from .models import Unit, Category, Currency, RozetkaCategory, availability_prom_help_text
from catalog.models import Manufacturer
from django.contrib.auth.models import User


class SetCourseForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    course = forms.CharField(label='Новый курс', widget=forms.NumberInput(
        attrs={'placeholder': 'Новый курс', 'step': '0.00001'},
    ))


class SetPricePercentForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    percent = forms.CharField(label='Процент', widget=forms.NumberInput(
        attrs={'placeholder': 'Процент', 'step': '0.01'},
    ))
    CHOICES = (('+', '+ (добавление)'),
               ('-', '- (вычитание)'))
    action_ = forms.ChoiceField(choices=CHOICES, widget=forms.Select())


class SetUnitForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(), required=True)


class SetCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(), required=True)


class SetAuthorForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(), required=True)


class SetRozetkaCategoryForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    category_rozetka = forms.ModelChoiceField(queryset=RozetkaCategory.objects.all(), widget=forms.Select(), required=True)


class SetCurrencyForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(), required=True)


class SetPriceForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    price = forms.CharField(label='Новая цена', widget=forms.NumberInput(
        attrs={'placeholder': 'Новая цена', 'step': '0.01'},
    ))


class SetPercentForOldPriceForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    percent = forms.CharField(label='Процент', widget=forms.NumberInput(
        attrs={'placeholder': 'Процент', 'step': '0.01'},
    ), required=False)


class SetAvailableFromPromForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    available = forms.CharField(label='Установите наличие', help_text=availability_prom_help_text)


class SetManufacturerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=forms.Select(), required=True)


class UpdateMizolPriceForm(forms.Form):
    file = forms.FileField(label='Файл')

    def __init__(self, *args, **kwargs):
        vendors = kwargs.pop('vendors', None)
        super(UpdateMizolPriceForm, self).__init__(*args, **kwargs)
        if vendors:
            self.fields['vendor_name'] = forms.CharField(widget=forms.Select(choices=vendors, attrs={
                'class': 'form-control'
            }), label='Вендор')
