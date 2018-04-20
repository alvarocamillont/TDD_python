from django.test import TestCase
from unittest.mock import patch


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_send_mail_to_adress_from_post(self, mock_send_email):
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertEqual(mock_send_email.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_email.call_args
        self.assertEqual(subject, 'Seu login para a superlista')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_sucess_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)

        message = list(response.context['messages'])[0]

        self.assertEqual(message.message, 'Verifique seu email, nós mandamos o link para vc acessar a sua lista')
        self.assertEqual(message.tags, 'success')
