from django import forms
from django.forms import ModelForm
from .models import Service, Process


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ('brand', 'model', 'error',)


class ProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = ('process', 'price',)
