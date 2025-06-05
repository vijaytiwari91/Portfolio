# Portfolio Security Implementation Guide

## 🔒 Security Features Implemented

This document outlines the comprehensive security measures implemented to protect your portfolio admin dashboard and ensure only authorized admin users can edit content.

## 1. Authentication & Authorization

### Admin-Only Access
- **Custom Login System**: Dedicated admin login at `/admin/login/` with enhanced security
- **Staff Member Required**: All dashboard views are protected with `@staff_member_required` decorator
- **Session Security**: 1-hour session timeout with automatic logout
- **Middleware Protection**: Custom middleware prevents unauthorized access to dashboard URLs

### Password Reset with Gmail OTP
- **Secure OTP System**: 6-digit OTP codes sent via Gmail
- **Time-Limited**: OTP expires in 10 minutes
- **Email Integration**: Uses Gmail SMTP for reliable delivery
- **Secure Flow**: Multi-step verification process

## 2. Session Management

### Enhanced Session Security
- **Automatic Timeout**: Sessions expire after 1 hour of inactivity
- **Activity Tracking**: Last activity timestamp updates on each request
- **Session Indicators**: Visual session status with warnings
- **Secure Cookies**: HTTPOnly and secure cookie settings

### Client-Side Monitoring
- **JavaScript Session Monitor**: Checks session status every 5 minutes
- **Auto-logout**: Redirects to login when session expires
- **Warning System**: Alerts users before session expiry

## 3. Security Headers & Middleware

### Custom Security Middleware
```python
# AdminSecurityMiddleware
- Validates admin authentication for dashboard URLs
- Enforces session timeouts
- Redirects unauthorized users

# SecurityHeadersMiddleware  
- Adds security headers to all responses
- Cache control for sensitive pages
- XSS and clickjacking protection
```

### Security Headers Applied
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`  
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Cache-Control: no-cache` (for dashboard pages)

## 4. Frontend Security

### Dashboard Security Features
- **Right-click Protection**: Disabled on dashboard pages
- **Developer Tools Protection**: F12, Ctrl+Shift+I, Ctrl+U disabled
- **Auto-save with Security**: Form auto-save with CSRF protection
- **Session Monitoring**: Real-time session status checks

### Navigation Security
- **Conditional Admin Menu**: Only shown to authenticated staff users
- **Dynamic Login/Logout**: Smart navigation based on auth status
- **Secure Redirects**: Proper redirect handling after login/logout

## 5. Email Configuration

### Gmail SMTP Setup
For production use, configure these settings in `settings.py`:

```python
# Uncomment and configure for production:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-admin-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use Gmail App Password
DEFAULT_FROM_EMAIL = 'Portfolio Admin <your-admin-email@gmail.com>'
```

### Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings > Security > App passwords
3. Generate a new app password for "Mail"
4. Use this app password (not your regular password) in Django settings

## 6. URL Security

### Protected Endpoints
All dashboard URLs require admin authentication:
- `/dashboard/*` - Main dashboard interface
- `/admin/login/` - Custom admin login
- `/admin/logout/` - Secure logout
- `/admin/password-reset/*` - OTP password reset system
- `/admin/profile/` - Admin profile management

### Public Endpoints
These remain publicly accessible:
- `/` - Home page
- `/about/` - About page  
- `/projects/` - Projects listing
- `/experience/` - Experience page
- `/contact/` - Contact form

## 7. Database Security

### User Model Protection
- Only staff users can access admin features
- Email required for OTP delivery
- Secure password hashing with Django's built-in system
- Last login tracking for security auditing

## 8. Production Considerations

### HTTPS Configuration
For production deployment, enable these settings:

```python
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Environment Variables
Move sensitive settings to environment variables:
- `SECRET_KEY`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- Database credentials

## 9. Admin Features

### Dashboard Capabilities
- **Content Management**: Edit About section, manage projects and skills
- **Statistics View**: Overview of portfolio content
- **Message Management**: Handle contact form submissions
- **Profile Settings**: Update admin profile and password
- **Quick Actions**: Fast access to common admin tasks

### Security Monitoring
- **Session Status**: Real-time session monitoring
- **Activity Tracking**: Last login information
- **Secure Logout**: Clear session data on logout
- **Auto-save Protection**: CSRF-protected form auto-saving

## 10. Testing the Security

### Verification Checklist
- [ ] Dashboard URLs redirect to login when not authenticated
- [ ] Non-staff users cannot access admin features
- [ ] Sessions expire after 1 hour of inactivity
- [ ] OTP password reset works with Gmail
- [ ] Admin dropdown only appears for staff users
- [ ] Secure headers are present in responses
- [ ] Form submissions include CSRF protection
- [ ] Auto-logout works when session expires

### Common Security Tests
1. Try accessing `/dashboard/` without logging in
2. Create a non-staff user and test access restrictions
3. Test session timeout by waiting 1 hour
4. Verify OTP emails are received correctly
5. Check browser developer tools for security headers

## 11. Troubleshooting

### Common Issues

**OTP Not Received:**
- Check Gmail SMTP settings
- Verify app password is correct
- Check spam folder
- Ensure email address is set for admin user

**Session Issues:**
- Clear browser cookies
- Check middleware order in settings
- Verify session backend is working

**Access Denied:**
- Ensure user has `is_staff = True`
- Check middleware configuration
- Verify URL patterns are correct

### Debug Mode
For development, emails are printed to console. Check terminal output for OTP codes when testing.

## 12. Security Best Practices

### Regular Maintenance
- Change admin passwords regularly
- Monitor access logs
- Keep Django updated
- Review user permissions periodically

### Additional Recommendations
- Use strong passwords (8+ characters, mixed case, numbers)
- Enable browser auto-lock on shared computers
- Regularly backup the database
- Monitor for suspicious login attempts

---

## 📧 Support

If you encounter any security issues or need assistance:
1. Check this documentation first
2. Review Django logs for error messages  
3. Test in a clean browser session
4. Verify all dependencies are installed correctly

**Remember**: Security is an ongoing process. Regularly review and update these measures as needed.
