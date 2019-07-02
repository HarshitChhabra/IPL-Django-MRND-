from django.views import View
from ipl_app.forms import LoginForm,SignUpForm
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render
from django.forms.utils import ErrorList
from django.contrib.auth.models import User


def LogOut(request):
    logout(request)
    return redirect("login")

class LoginView(View):

    def get(self,request,*args,**kwargs):
        if(request.user.is_authenticated):
            return redirect('/seasons')
        loginForm = LoginForm()
        return render(
            request,
            template_name="login.html",
            context={
                'loginForm':loginForm
            }
        )

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("seasons")
            else:

                return render(
                    request,
                    template_name="login.html",
                    context={
                        'loginForm': form,
                        'authError':'Authentication Failed. Invalid credentials'
                    }
                )
        else:
            return render(
                request,
                template_name="login.html",
                context={
                    'loginForm':form
                }
            )


class SignUpView(View):

    def get(self,request,*args,**kwargs):
        if (request.user.is_authenticated):
            return redirect('/seasons')
        signUpForm = SignUpForm()
        return render(
            request,
            template_name="signup.html",
            context={
                'signUpForm':signUpForm
            }
        )

    def post(self,request,*args,**kwargs):
        signUpForm = SignUpForm(request.POST)
        if signUpForm.is_valid():
            user = User.objects.create_user(**signUpForm.cleaned_data)
            login(request,user)
            return redirect("seasons")