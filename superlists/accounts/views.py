from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        f'{reverse(login)}?token={token.uid}'
    )
    message_body = f'Use esse link para log in:\n\n{url}'
    send_mail(
        'Seu link de login para SuperList',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(request, 'Verifique seu email, nós mandamos o link para vc acessar a sua lista')
    return redirect('/')


def login(request):

    return redirect('/')
