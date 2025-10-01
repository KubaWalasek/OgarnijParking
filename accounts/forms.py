from django.contrib.auth import get_user_model, forms
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']


class UpdateUserForm(forms.ModelForm):

    password1 = forms.CharField(label='Nowe hasło', widget=forms.PasswordInput, required=False, help_text='Zostaw puste, jeśli nie chcesz zmieniać hasła')
    password2 = forms.CharField(label='Powtórz nowe hasło', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('Hasła nie pasują do siebie!')
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









