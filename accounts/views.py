from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from recipes.models import Recipe


def login_view(request):
    """
    Custom login view that checks if username exists
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
        else:
            messages.error(request, 'Username does not exist. Please register first.')
        
    return render(request, 'accounts/login.html')


def register(request):
    """
    View for user registration with simple alert for existing username
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" already exists. Please log in instead.')
            return redirect('login')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" is already registered. Please use a different email.')
            return render(request, 'accounts/register.html')
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')
        
        # Check password length
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/register.html')
        
        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            
    return render(request, 'accounts/register.html')


@login_required
def profile(request):
    """
    View for displaying user profile
    """
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'accounts/profile.html', {'recipes': user_recipes})


@login_required
def edit_profile(request):
    """
    View for editing user profile
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)