import random
import string
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.cache import cache
import json

def generate_otp(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))

def admin_login_view(request):
    """Custom admin login with enhanced security"""
    print(f"DEBUG: Login attempt - Method: {request.method}")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"DEBUG: Username: '{username}', Password length: {len(password) if password else 0}")
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(f"DEBUG: Authentication result: {user}")
            
            if user is not None and user.is_staff:
                login(request, user)
                print(f"DEBUG: Login successful for {user.username}")
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('portfolio:dashboard_home')
            else:
                print(f"DEBUG: Login failed - User: {user}, Is Staff: {user.is_staff if user else 'N/A'}")
                messages.error(request, 'Invalid credentials or insufficient permissions.')
        else:
            print(f"DEBUG: Missing credentials")
            messages.error(request, 'Please provide both username and password.')
    
    print(f"DEBUG: Rendering login template")
    return render(request, 'admin/auth/login.html')

def admin_logout_view(request):
    """Custom admin logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portfolio:home')

def password_reset_request(request):
    """Request password reset with OTP"""
    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            user = User.objects.get(username=username, is_staff=True)
            
            # Generate OTP
            otp = generate_otp()
            
            # Store OTP in cache for 10 minutes
            cache_key = f'password_reset_otp_{user.id}'
            cache.set(cache_key, otp, 600)  # 10 minutes
            
            # Send OTP via email
            subject = 'Portfolio Admin - Password Reset OTP'
            message = f"""
Hello {user.first_name or user.username},

You have requested a password reset for your portfolio admin account.

Your OTP code is: {otp}

This code will expire in 10 minutes.

If you didn't request this password reset, please ignore this email.

Best regards,
Portfolio Admin System
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL or 'noreply@portfolio.com',
                    [user.email],
                    fail_silently=False,
                )
                
                # Store user ID in session for verification step
                request.session['reset_user_id'] = user.id
                messages.success(request, 'OTP has been sent to your email address.')
                return redirect('portfolio:password_reset_verify')
                
            except Exception as e:
                messages.error(request, 'Failed to send email. Please try again later.')
                print(f"Email error: {e}")  # For debugging
                
        except User.DoesNotExist:
            # Don't reveal if username exists or not
            messages.error(request, 'If this username exists and is an admin, an OTP will be sent.')
    
    return render(request, 'admin/auth/password_reset_request.html')

def password_reset_verify(request):
    """Verify OTP and allow password reset"""
    if 'reset_user_id' not in request.session:
        messages.error(request, 'Invalid reset session. Please start over.')
        return redirect('portfolio:password_reset_request')
    
    user_id = request.session['reset_user_id']
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'admin/auth/password_reset_verify.html')
        
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'admin/auth/password_reset_verify.html')
        
        # Verify OTP
        cache_key = f'password_reset_otp_{user_id}'
        stored_otp = cache.get(cache_key)
        
        if stored_otp and stored_otp == otp_entered:
            try:
                user = User.objects.get(id=user_id, is_staff=True)
                user.set_password(new_password)
                user.save()
                
                # Clear the OTP from cache
                cache.delete(cache_key)
                
                # Clear session
                del request.session['reset_user_id']
                
                messages.success(request, 'Password reset successfully! You can now login with your new password.')
                return redirect('portfolio:admin_login')
                
            except User.DoesNotExist:
                messages.error(request, 'Invalid user. Please start over.')
                return redirect('portfolio:password_reset_request')
        else:
            messages.error(request, 'Invalid or expired OTP. Please try again.')
    
    return render(request, 'admin/auth/password_reset_verify.html')

@staff_member_required
def admin_profile(request):
    """Admin profile management"""
    if request.method == 'POST':
        user = request.user
        
        # Update basic info
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Password change
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            else:
                user.set_password(new_password)
                messages.success(request, 'Password updated successfully!')
        
        user.save()
        
        if not any(messages.get_messages(request)):
            messages.success(request, 'Profile updated successfully!')
    
    return render(request, 'admin/auth/profile.html', {'user': request.user})

@require_POST
def check_session_status(request):
    """AJAX endpoint to check if user session is still valid"""
    if request.user.is_authenticated and request.user.is_staff:
        return JsonResponse({'authenticated': True})
    return JsonResponse({'authenticated': False})

def admin_login_debug_view(request):
    """Simple debug login view without fancy styling"""
    print(f"DEBUG: Login debug attempt - Method: {request.method}")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"DEBUG: Username: '{username}', Password length: {len(password) if password else 0}")
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            print(f"DEBUG: Authentication result: {user}")
            
            if user is not None and user.is_staff:
                login(request, user)
                print(f"DEBUG: Login successful for {user.username}")
                messages.success(request, f'DEBUG: Login successful! Welcome {user.username}')
                return redirect('portfolio:dashboard_home')
            else:
                print(f"DEBUG: Login failed - User: {user}, Is Staff: {user.is_staff if user else 'N/A'}")
                messages.error(request, f'DEBUG: Auth failed. User found: {user is not None}, Is staff: {user.is_staff if user else "N/A"}')
        else:
            print(f"DEBUG: Missing credentials")
            messages.error(request, 'DEBUG: Please provide both username and password.')
    
    print(f"DEBUG: Rendering debug login template")
    return render(request, 'admin/auth/login_debug.html')
