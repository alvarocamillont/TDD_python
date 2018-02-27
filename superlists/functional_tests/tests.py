import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from unittest import skip

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f'http://{staging_server}'

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # João ouviu falar de uma nova aplicação online para lista de tarefas
        # Ele decide entra na homepage
        self.browser.get(self.live_server_url)

        # Ele percebe que o título da página e o cabeçalho mencionam lista de tarefas (to-do)
        self.assertIn('To-Do list', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Sua Lista', header_text)

        # Ele é convidado a inserir um item de tarefa
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Entre com um item na lista'
        )
        # Ele digita "Comprar penas de pavão" em uma caixa de texto
        inputbox.send_keys('Comprar penas de pavão')

        # Quando ele aperta enter, a pagina é atualizada e agora a pagina lista
        # 1: Comprar penas de pavão como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_list_table('1: Comprar penas de pavão')

        # Ainda há uma caixa de texto e ele acrescenta "Fazer isca de pesca"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Fazer isca de pesca')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #  A página é atualizada novamente e agora mostra dois itens na lista
        self.wait_for_row_in_list_table('1: Comprar penas de pavão')
        self.wait_for_row_in_list_table('2: Fazer isca de pesca')

        # João se pergunta se o site irá lembrar dessa lista. Então ele percebe que o site gerou um
        # url único para ele - há um texto explicando isso

        # Satisfeito ele vai durmir

    def test_multiple_users_can_start_lists_at_differnt_url(self):
        # Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar penas de pavão')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Ela percebe que sua lista tem um URL ùnico
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Agora um novo usuario Francis, chega ao site
        # Usamos uma nova sessão do navegardor para garantir que nenhuma informação está vindo de coockie e etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis acessa a página inicial, Não há nenhumsina da lista da Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar penas de pavão', page_text)
        self.assertNotIn('Fazer isca de pesca', page_text)

        # Francis começa uma lista nova
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar leite')

        # Francis obtem o proprio url exclusivo
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Novamente não há sinal da lista da edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar penas de pavão', page_text)
        self.assertIn('Comprar leite', page_text)


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith acessa a página inicial
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Ela percebe que a caixa de entrada está elegantemente centralizada
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # Ela inicia uma nova lista e vê a entrada está elegantemente centralizada também
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # Edith acessa a pagina principal e acidentalmente tenta submeter
        # um item vazio na lista. Ela tecla ENter na caixa de entrada vazia

        # A página inicial é atualizada e há uma mensagem de erro informando
        # que itens da lista não podem estar em branco

        # ELa tenta novamente com um texto para o item, e isso agora funciona

        # De forma perversa, ela agora decide submeter um segundo item em branco na lista

        # Ela recebe um aviso semelhante na página da lista

        # E ela pode corrigir isso preenchendo o item com um texto
        self.fail('Me escreva!')
