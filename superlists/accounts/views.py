from django.shortcuts import redirect
from django.core.mail import send_mail

# Create your views here.
def send_login_email(request):
    return redirect('/')