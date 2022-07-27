from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from app_put_into_good_hand.models import Donation, Institution, User
from app_put_into_good_hand.forms import RegisterForm


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
        return render(request, "index.html", {"quantity": quantity, "count_institutions": count_institutions,
                                            "fundations": fundations, "organizations": organizations, "locals": locals})


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html",  {})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                User.objects.create_user(mail, password)
                return HttpResponse(f'Użytkownik {mail} został zarejestrowany.')
        return render(request, "register.html", {"form": form})
