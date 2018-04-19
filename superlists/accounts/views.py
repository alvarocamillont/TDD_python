from django.shortcuts import redirect
from django.core.mail import send_mail


def send_login_email(request):
    email = request.POST['email']

    send_mail(
        'Seu login para a superlista',
        'body text tbc',
        'noreply@superlists',
        [email],
    )
    return redirect('/')