from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """
    Custom decorator that ensures user is authenticated and is staff,
    redirecting to our custom login page if not.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this area.')
            return redirect('portfolio:admin_login')
        
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this area.')
            return redirect('portfolio:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def admin_login_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the log-in page if necessary.
    """
    def check_staff(user):
        return user.is_active and user.is_staff
    
    actual_decorator = user_passes_test(
        check_staff,
        login_url=login_url or '/auth/login/',
        redirect_field_name=redirect_field_name,
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator
