from importlib import import_module
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, ChangePasswordForm, ContactFrom, LoginForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.conf import settings
from posts.models import Service


@login_required(login_url='login')
def UserProfile(request, username):
    return render(request, 'account/userprofile.html')


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                username=username, password=password)
            user = authenticate(username=username, password=password, )
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.company_name = form.cleaned_data.get('company_name')
            user.profile.phone_number = form.cleaned_data.get('phone_number')

            login(request, user)
            messages.success(request, 'Kayıt Başarılı... Hoşgeldiniz')
            return redirect('index')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }

    return render(request, 'account/signup.html', context)


def Login(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            user.profile.active = True
            user.profile.save()
            messages.success(request, "Başarı ile giriş yaptınız")
            login(request, user)
            return redirect("index")
        messages.success(request, "Kullanıcı Bulunamadı.")
        return render(request, "account/login.html", context)
    return render(request, "account/login.html", context)


@login_required(login_url='login')
def Logout(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("index")


@login_required(login_url='login')
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parola Değiştirme Başarılı.')

            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'account/change_password.html', context)


@login_required(login_url='login')
def Contact(request):
    form = ContactFrom(request.POST or None)
    if form.is_valid():
        subject = "Website Inquiry"
        body = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'message': form.cleaned_data['message'],
        }
        message = "\n".join(body.values())
        try:
            send_mail(subject, message, 'cinarkombiticaret35@gmail.com',
                      ['cinarkombiticaret35@gmail.com'])
            messages.success(request, 'Mesajınız Gönderildi.')
        except BadHeaderError:
            return HttpResponse('Mesaj Gönderilemedi.Lütfen Tekrar Deneyiniz...')
        return redirect("index")

    else:
        form = ContactFrom()

    context = {
        'form': form,
    }
    return render(request, 'account/contact.html', context)


@login_required(login_url='login')
def EditProfile(request, username):
    user = Profile.objects.get(user__username=username)
    form = EditProfileForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "Bilgiler Kaydedildi.")
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        form = EditProfileForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'account/editprofile.html', context)


def whatsapp(request):
    return redirect("https://api.whatsapp.com/send?phone=+90-534-745-34-69")


@login_required(login_url='login')
def PhoneNumberList(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'account/phonenumbers.html', context)
