from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, StorageUpdateForm, ProfileUserUpdateForm
from storage.models import Teammates

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Saves the user to the database
            login(request, user)  # Logs the new user in on the spot
            return redirect('profile')
    else:
        # This handles the GET request when a user first visits the page
        form = UserRegisterForm()
        
    # This return statement must be outside the if/else conditions
    return render(request, 'user/register.html', {'form': form})
        
        
def profile(request):
     user_storage_records = Teammates.objects.filter(author = request.user)

     context = {
          'records': user_storage_records
     }
     return render(request, 'user/profile.html',context)

@login_required
def edit_profile(request):
    # Fetch the specific active storage row item for this user
    storage_instance = Teammates.objects.filter(author=request.user).first()

    if request.method == 'POST':
        u_form = ProfileUserUpdateForm(request.POST, instance=request.user)
        s_form = StorageUpdateForm(request.POST, instance=storage_instance)

        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            
            # Catch instance creation fallback safety check
            storage_item = s_form.save(commit=False)
            if not storage_item.pk:
                storage_item.author = request.user
            storage_item.save()
            
            messages.success(request, "Your profile fields have been updated successfully!")
            return redirect('profile')
    else:
        u_form = ProfileUserUpdateForm(instance=request.user)
        s_form = StorageUpdateForm(instance=storage_instance)

    context = {
        'u_form': u_form,
        's_form': s_form
    }
    return render(request, 'user/edit_profile.html', context)


