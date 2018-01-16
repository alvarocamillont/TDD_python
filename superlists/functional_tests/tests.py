import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # João ouviu falar de uma nova aplicação online para lista de tarefas
        # Ele decide entra na homepage
        self.browser.get(self.live_server_url)

        # Ele percebe que o título da página e o cabeçalho mencionam lista de tarefas (to-do)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Sua Lista', header_text)

        # Ele é convidado a inserir um item de tarefa
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Entre um item na sua lista'
        )
        # Ele digita "Comprar penas de pavão" em uma caixa de texto
        inputbox.send_keys('Comprar penas de pavão')

        # Quando ele aperta enter, a pagina é atualizada e agora a pagina lista
        # 1: Comprar penas de pavão como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Comprar penas de pavão')

        # Ainda há uma caixa de texto e ele acrescenta "Fazer isca de pesca"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Fazer isca de pesca')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #  A página é atualizada novamente e agora mostra dois itens na lista
        self.check_for_row_in_list_table('1: Comprar penas de pavão')
        self.check_for_row_in_list_table('2: Fazer isca de pesca')

        # João se pergunta se o site irá lembrar dessa lista. Então ele percebe que o site gerou um
        # url único para ele - há um texto explicando isso
        self.fail("Teste Encerrado!")  # Final cap 5
        # Ele acessa a url e verifica que sua lista continua lá

        # Satisfeito ele vai durmir
