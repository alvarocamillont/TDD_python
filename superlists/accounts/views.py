from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages


def send_login_email(request):
    email = request.POST['email']
    send_mail(
        'Seu link de login para SuperList',
        'Use esse link para log in',
        'noreply@superlists',
        [email],
    )
    messages.success(request, 'Verifique seu email, nós mandamos o link para vc acessar a sua lista')
    return redirect('/')