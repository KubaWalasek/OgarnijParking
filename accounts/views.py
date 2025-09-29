from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import RegisterUserForm, LoginUserForm, UpdateUserForm
from accounts.models import UserProfile


######################################################################################################
class RegisterView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'register'
        })

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password_1'])
            user.save()
            UserProfile.objects.create(user=user,
                                       first_name=form.cleaned_data['first_name'],
                                       last_name=form.cleaned_data['last_name'],
                                       post_code=form.cleaned_data['post_code'],
                                       city=form.cleaned_data['city'],
                                       street=form.cleaned_data['street'],
                                       street_number=form.cleaned_data['street_number'],
                                       door_number=form.cleaned_data['door_number'],
                                       phone_number=form.cleaned_data['phone_number'],

                                       )
            messages.success(request, 'Account created successfully!')
            return redirect('user_account')
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'register',

        })

######################################################################################################
class LoginView(View):
    def get(self, request):
        form = LoginUserForm()
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'login'
        })

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if request.user.is_authenticated and request.user.username == username and user is not None :
                return render(request, 'account_form.html', {
                    'form': form,
                    'message': 'You are already logged in !',
                    'url': 'login'
                })

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'user_account')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password !')
                return render(request, 'account_form.html', {
                    'form': form,
                    'url': 'login'
                })
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'login'
        })

######################################################################################################
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


######################################################################################################
class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        initial_data = {
            'username': user.username,
            'email': user.email,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'post_code': profile.post_code,
            'city': profile.city,
            'street': profile.street,
            'street_number': profile.street_number,
            'door_number': profile.door_number,
            'phone_number': profile.phone_number,
        }
        form = UpdateUserForm(initial=initial_data)

        form.fields['password_1'].required = False
        form.fields['password_2'].required = False
        form.fields['email'].required = False
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'user_account'
        })

    def post(self, request):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            # brak zmian w polach modelu i brak prób zmiany hasła
            if not form.changed_data and not (
                    form.cleaned_data.get('password_1') or form.cleaned_data.get('password_2')
            ):
                messages.info(request, 'No data updated')
                return render(request, 'account_form.html', {
                    'form': form,
                    'url': 'user_account'
                })

            # zmiana hasła tylko gdy oba pola wypełnione (spójne i zwalidowane przez form)
            if form.cleaned_data.get('password_1') and form.cleaned_data.get('password_2'):
                user.set_password(form.cleaned_data['password_1'])

            # zapisz użytkownika (np. zmiana email)
            user.save()

            # aktualizacje profilu (nie są częścią modelu User)
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.post_code = form.cleaned_data.get('post_code')
            profile.city = form.cleaned_data.get('city')
            profile.street = form.cleaned_data.get('street')
            profile.street_number = form.cleaned_data.get('street_number')
            profile.door_number = form.cleaned_data.get('door_number')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()

            # utrzymanie sesji po zmianie hasła
            update_session_auth_hash(request, user)
            messages.success(request, 'Account updated successfully!')
            return redirect('user_account')

        # tu trafisz tylko przy błędach walidacji
        messages.error(request, 'Invalid data!')
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'user_account'
        })
