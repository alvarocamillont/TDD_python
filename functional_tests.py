import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # João ouviu falar de uma nova aplicação online para lista de tarefas
        # Ele decide entra na homepage
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Comprar penas de pavão', [row.text for row in rows])

        # Ainda há uma caixa de texto e ele acrescenta "Fazer isca de pesca"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Fazer isca de pesca')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        #  A página é atualizada novamente e agora mostra dois itens na lista
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Comprar penas de pavão', [row.text for row in rows])
        self.assertIn('2: Fazer isca de pesca', [row.text for row in rows])

        # João se pergunta se o site irá lembrar dessa lista. Então ele percebe que o site gerou um
        # url único para ele - há um texto explicando isso
        self.fail("Teste Encerrado!")
        # Ele acessa a url e verifica que sua lista continua lá

        # Satisfeito ele vai durmir


def main():
    unittest.main(warnings='ignore')


if __name__ == '__main__':
    main()
