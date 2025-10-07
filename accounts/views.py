from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import CreateUserForm, UpdateUserForm, AdresForm, DeleteUserForm, LoginForm, UpdatePasswordForm
from accounts.models import Adres


######################################################################################################

def home(request):
    return render(request, 'home_base.html')


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'register'
        })

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_account')
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'register',
        })

######################################################################################################
class LoginView(View):
    def _login_set(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in!')
            return redirect('user_account')

        if request.method == 'GET':
            form = LoginForm()
            return render(request, 'account_form.html', {
                'form': form,
                'url': 'login'
            })

        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'You are logged in!')
                return redirect('user_account')
            messages.error(request, 'Invalid username or password!')
            return render(request, 'account_form.html', {
                'form': form,
                'url': 'login'
            })

    def get(self, request):
        return self._login_set(request)

    def post(self, request):
        return self._login_set(request)




######################################################################################################
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


######################################################################################################
class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = UpdateUserForm(instance=user)
        adres, created = Adres.objects.get_or_create(user=user)
        adres_form = AdresForm(instance=adres)
        return render(request, 'account_form.html', {
            'form': form,
            'adres_form': adres_form,
            'url': 'user_account'
        })

    def post(self, request):
        user = request.user
        adres, _ = Adres.objects.get_or_create(user=user)
        form = UpdateUserForm(request.POST, instance=user)
        adres_form = AdresForm(request.POST, instance=adres)
        if form.is_valid() and adres_form.is_valid():
            if not form.has_changed() and  not adres_form.has_changed():
                messages.success(request, 'No data updated !')
                return redirect('user_account')
            form.save()
            adres_form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('user_account')
        return render(request, 'account_form.html', {
            'form': form,
            'adres_form': adres_form,
            'url': 'user_account',
        })

class UpdatePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdatePasswordForm(request.user)
        return render(request, 'update_password.html', {'form': form})

    def post(self, request):
        form = UpdatePasswordForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password updated successfully!')
            return redirect('user_account')
        return render(request, 'update_password.html', {'form': form})

class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request):
        form = DeleteUserForm(user=request.user)
        return render(request, 'delete_account.html', {
            'form': form,
        })

    def post(self, request):
        form = DeleteUserForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.delete()
            messages.success(request, 'Account deleted successfully!')
            return redirect('login')
        return render(request, 'delete_account.html', {
            'form': form,
        })