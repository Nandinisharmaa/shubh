from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from shop.models import Customer


class PasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False,
                                   widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                                                     'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}), )
    new_password2 = forms.CharField(label=_("Confirm Password"),
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}))


class Passwordreset(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=300,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))


class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"),
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm Password"),
                                    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                                                      'class': 'form-control'}))


# Customer profile form
class CustomerProfileform(forms.ModelForm):
 class Meta:
    model = Customer
    fields = ['name', 'locality','city', 'zipcode', 'state']
    widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
               'locality': forms.TextInput(attrs={'class': 'form-control'}),
               'city':forms.TextInput(attrs={'class':'form-control'}),
               'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
               'state': forms.Select(attrs={'class': 'form-control'})}
