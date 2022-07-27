from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from app_put_into_good_hand.models import Donation, Institution, User
from app_put_into_good_hand.forms import RegisterForm, LoginForm


class LandingPageView(View):
    def get(self, request):
        gifts = Donation.objects.all()
        quantity = 0
        institutions = []
        for gift in gifts:
            quantity += gift.quantity
            if gift.institution not in institutions:
                institutions.append(gift.institution.name)
        count_institutions = len(institutions)
        fundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        locals = Institution.objects.filter(type=3)
        user = request.user
        return render(request, "index.html", {"quantity": quantity, "count_institutions": count_institutions, "user": user,
                                            "fundations": fundations, "organizations": organizations, "locals": locals})


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "form.html",  {"user": user})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        user = request.user
        return render(request, "login.html", {"form": form, "user": user})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['mail'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                next_parameter = request.GET.get('next')
                if next_parameter:
                    return redirect(next_parameter)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/register')
        return render(request, "login.html", {'form': form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        user = request.user
        return render(request, "register.html", {"form": form, "user": user})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                User.objects.create_user(mail, password)
                return HttpResponseRedirect("/login")
        return render(request, "register.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
