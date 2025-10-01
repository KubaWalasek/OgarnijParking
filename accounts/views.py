from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import CreateUserForm, UpdateUserForm



######################################################################################################

def home(request):
    return render(request, 'base.html')


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
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_account')
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'register',
        })

######################################################################################################
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in!')
            return redirect('user_account')
        form = AuthenticationForm()
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'login'
        })

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in!')
            return redirect('user_account')

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are logged in!')
            return redirect('user_account')

        messages.error(request, 'Invalid username or password!')
        return render(request, 'account_form.html',{
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
        form = UpdateUserForm(instance=request.user)
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'user_account'
        })

    def post(self, request):
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account changed successfully!')
            return redirect('user_account')
        return render(request, 'account_form.html', {
            'form': form,
            'url': 'user_account',
        })