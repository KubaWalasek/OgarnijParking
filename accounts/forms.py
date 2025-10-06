from django.contrib.auth import get_user_model, forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import Adres

User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']


class UpdateUserForm(forms.ModelForm):

    old_password = forms.CharField(label='Stare hasło', widget=forms.PasswordInput, required=False, help_text='Wprowadź stare hasło, aby potwierdzić zmiany')
    password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput, required=False, help_text='Zostaw puste, jeśli nie chcesz zmieniać hasła')
    password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if not old_password:
                raise forms.ValidationError('Nie podano starego hasła!')
            if not self.user_instance.check_password(old_password):
                raise forms.ValidationError('Nieprawidłowe stare hasło.')
            if password1 != password2:
                raise forms.ValidationError('Nowe hasła nie pasują do siebie!')
            if len(password1) < 8:
                raise forms.ValidationError('Hasło musi mieć min. 8 znaków')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')

        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user

class AdresForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = ['post_code', 'city', 'street', 'house_number', 'apartment_number']




class DeleteUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user_instance or not self.user_instance.check_password(password):
            raise forms.ValidationError('Nieprawidłowe hasło.')
        return password





