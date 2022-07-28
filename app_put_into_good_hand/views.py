from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from app_put_into_good_hand.models import Donation, Institution, User, Category


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
        conn = {
            "quantity": quantity,
            "count_institutions": count_institutions,
            "user": user,
            "fundations": fundations,
            "organizations": organizations,
            "locals": locals
        }
        return render(request, "index.html", conn)


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        categoried = Category.objects.all()
        institutions = Institution.objects.all()
        conn = {
            "user": user,
            "categoried": categoried,
            "institutions": institutions,
        }
        return render(request, "form.html",  conn)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['mail']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponseRedirect('/register')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('name') and request.POST.get('surname') and request.POST.get('mail') \
                and request.POST.get('password') and request.POST.get('password2'):
            users = User.objects.all()
            used = False
            for us in users:
                if us.username == request.POST.get('mail'):
                    used = True
            if used:
                return HttpResponse("Mail został już wykorzystany.")
            else:
                if request.POST.get('password') == request.POST.get('password2'):
                    User.objects.create_user(email=request.POST.get('mail'),
                                             password=request.POST.get('password'),
                                             first_name=request.POST.get('name'),
                                             last_name=request.POST.get('surname'))
                    return HttpResponseRedirect('/login')
                else:
                    return HttpResponse("Hasła nie są identyczne.")
        else:
            return HttpResponseRedirect('/register')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class UserView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "profile.html", {"user": user})
