from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm

# Create your views here.


# function for the registration form
# def register(request):
#     if request.method=="POST":
#         form=RegistrationForm(request.POST)
#         procForm=profileForm(request.POST, request.FILES)
#         if form.is_valid() and procForm.is_valid():
#             username=form.cleaned_data.get('username')
#             user=form.save()
#             profile=procForm.save(commit=False)
#             profile.user=user
#             profile.save()

#             # messages.success(request, f'Successfully created Account!.You can now login as {username}!')
#         return redirect('login')
#     else:
#         form= RegistrationForm()
#         prof=profileForm()
#     params={
#         'form':form,
#         'profForm': prof
#     }
#     return render(request, 'registration/register.html', params)


def index(request):
    return render(request, 'main/index.html')