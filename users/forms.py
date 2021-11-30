from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


def UniqueEmail(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('Bu e-mail adresine sahip bir kullanıcı mevcut')


def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('Bu kullanıcı adına sahip bir kullanıcı mevcut.')


class SignupForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(), max_length=30, required=True, label="Kullanıcı Adı")
    full_name = forms.CharField(label='İsim Soyisim')
    company_name = forms.CharField(label='Firma Adı')
    phone_number = forms.CharField(label='Telefon Numarası', widget=forms.TextInput(attrs={
                                   'placeholder': '05555555555'}))
    password = forms.CharField(widget=forms.PasswordInput(), label="Parola")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Parola Doğrulama")

    class Meta:
        model = User
        fields = ('username', 'full_name', 'company_name', 'phone_number', 'password',
                  'confirm_password',)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Parola Eşleşmedi. Lütfen Tekrar Deneyiniz.'])
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input is-medium'}), label="Eski Parola", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input is-medium'}), label="Yeni Parola", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input is-medium'}), label="Parola Doğrulama", required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(
                ['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] = self.error_class(
                ['Passwords do not match.'])
        return self.cleaned_data


class ContactFrom(forms.Form):
    name = forms.CharField(max_length=40, label="İsim Soyisim")
    email = forms.EmailField(max_length=100, label="E-Posta Adresi")
    message = forms.CharField(widget=forms.Textarea(), label='Mesajınız')


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('full_name', 'company_name', 'phone_number',)
