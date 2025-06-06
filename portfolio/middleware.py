from django.shortcuts import redirect
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import time

class AdminSecurityMiddleware(MiddlewareMixin):
    """
    Enhanced security middleware for admin dashboard access
    """
    def process_request(self, request):
        # Define admin paths that require authentication
        admin_paths = ['/dashboard/', '/admin/']
          # Exclude certain admin paths from authentication check
        excluded_paths = ['/admin/login/', '/admin/logout/', '/admin/password-reset/', '/auth/', '/dashboard/debug/']
        
        # Check if accessing protected admin URLs
        is_admin_path = any(request.path.startswith(path) for path in admin_paths)
        is_excluded_path = any(request.path.startswith(path) for path in excluded_paths)
        
        if is_admin_path and not is_excluded_path:
            # Ensure user is authenticated and is staff
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this area.')
                return redirect('portfolio:admin_login')
            
            if not request.user.is_staff:
                messages.error(request, 'You do not have permission to access this area.')
                return redirect('portfolio:home')
            
            # Check session timeout (1 hour)
            if 'last_activity' in request.session:
                last_activity = request.session['last_activity']
                if time.time() - last_activity > 3600:  # 1 hour
                    request.session.flush()
                    messages.error(request, 'Your session has expired. Please log in again.')
                    return redirect('portfolio:admin_login')
            
            # Update last activity
            request.session['last_activity'] = time.time()
        
        return None

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    
    def process_response(self, request, response):
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Add cache control for admin and dashboard pages
        if request.path.startswith('/dashboard/') or request.path.startswith('/admin/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response
