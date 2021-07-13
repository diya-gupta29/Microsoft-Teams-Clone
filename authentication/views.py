from django.shortcuts import render
from django.views import View
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User

class registration_view(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request, 'authentication/reg.html',{'form':form})
    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'authentication/reg.html',{'form':form})
