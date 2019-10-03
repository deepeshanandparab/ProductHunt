from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import RegistrationForm
from .models import Profile
from .forms import ProfileUpdateForm

def registerPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created sucessfully for {username}. You can login now.')
            return redirect('log_in_page')
    else:
        form = RegistrationForm()
    context = {'form': form, 'title': 'Registration'}
    return render(request, 'accounts/register.html', context)


def logInPage(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Username or Password is incorrect!')
            return render(request, 'accounts/login.html', {'title':'Login'})
    else:
        return render(request, 'accounts/login.html', {'title':'Login'})

def logOutPage(request):
        auth.logout(request)
        return redirect('home_page')

@login_required
def updateProfilePage(request, id):
    profile = Profile.objects.get(user_id=id)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile has been updated successfully.')
        return redirect('my_product_page')
    context = {'title':'Profile Update', 'form':form}
    return render(request, 'accounts/update_profile.html', context)




