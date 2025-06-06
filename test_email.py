#!/usr/bin/env python
"""
Simple script to test Django's email functionality.
Run this script with `python test_email.py` from the project root.
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
django.setup()

# Import Django components
from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test Django's email functionality"""
    print("Testing email configuration...")
    print(f"Email backend: {settings.EMAIL_BACKEND}")
    
    try:
        # Send a test email
        send_mail(
            subject="Test Email from Portfolio",
            message="This is a test email to verify that the email configuration is working correctly.",
            from_email="noreply@vijayportfolio.com",
            recipient_list=["gvedhanth123@gmail.com"],
            fail_silently=False,
        )
        print("Test email sent successfully! Check your console output or email inbox.")
    except Exception as e:
        print(f"Error sending test email: {e}")
        print("Make sure your email settings are correct in settings.py.")

if __name__ == "__main__":
    test_email()
