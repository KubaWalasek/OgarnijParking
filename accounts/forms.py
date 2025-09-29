from django import forms
from django.contrib.auth.models import User

######################################################################################################

class RegisterUserForm(forms.ModelForm):
    required_css_class = 'required'
    username = forms.CharField(required=True)
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    post_code = forms.CharField(max_length=10, required=False)
    city = forms.CharField(max_length=30, required=False)
    street = forms.CharField(max_length=30, required=False)
    street_number = forms.CharField(max_length=10, required=False)
    door_number = forms.CharField(max_length=10, required=False)
    phone_number = forms.CharField(max_length=15, required=False)





    def clean_password_1(self):
        password_1 = self.cleaned_data.get('password_1')
        if password_1 is None:
            return
        if len(password_1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not any(c.isupper() for c in password_1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        return password_1

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        # jeśli password_1 ma błędy - nie porównuj
        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError('Passwords do not match !')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Użytkownik z tym adresem e-mail już istnieje')
        return email

    class Meta:
        model = User
        fields = ['username', 'email']

######################################################################################################

class LoginUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

############################################################################################################


class UpdateUserForm(forms.ModelForm):
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password_2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=True, error_messages={'required': 'Email is required'})
    first_name = forms.CharField(max_length=20, required=False )
    last_name = forms.CharField(max_length=20,required=False )
    post_code = forms.CharField(max_length=10, required=False )
    city = forms.CharField(max_length=30, required=False)
    street = forms.CharField(max_length=30, required=False)
    street_number = forms.CharField(max_length=10, required=False)
    door_number = forms.CharField(max_length=10, required=False)
    phone_number = forms.CharField(max_length=15, required=False)



# Python
    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password_1')
        password_2 = cleaned_data.get('password_2')

        # brak zmiany hasła
        if not password_1 and not password_2:
            return cleaned_data

        # podano tylko jedno pole
        if (password_1 and not password_2) or (password_2 and not password_1):
            raise forms.ValidationError('Provide both password fields.')

        # pełna walidacja przy zmianie
        if password_1 != password_2:
            raise forms.ValidationError('Passwords do not match !')
        if len(password_1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not any(c.isupper() for c in password_1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email']
