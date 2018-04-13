from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'judite@exemplo.com'
SUBJECT = 'Seu link de login para SuperList'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Judite acesse o incrivel site de superlistas
        # e, pela primeira vez, percebe que há uma seção de Login na barra
        # de navegação. Essa seção está lhe dizendo para inserir o seu
        # email, portanto ela faz isso
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Uma mensagem aparece informando que um email foi enviado
        self.wait_for(lambda: self.assertIn(
            'Verifique seu email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Ela verifica seu email e encontra uma mensagem
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # A mensagem contem um link com um url
        self.assertIn('Use esse link para log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Não foi possivel encontra o link no email:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Ela clica no url
        self.browser.get(url)

        # Ela está logada!
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log Out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

