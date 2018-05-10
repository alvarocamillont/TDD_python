from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Edith acessa a pagina principal e acidentalmente tenta submeter
        # um item vazio na lista. Ela tecla ENter na caixa de entrada vazia
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # A página inicial é atualizada e há uma mensagem de erro informando
        # que itens da lista não podem estar em branco
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # ELa tenta novamente com um texto para o item, e isso agora funciona
        self.get_item_input_box().send_keys('Compre Leite')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Compre Leite')
        # De forma perversa, ela agora decide submeter um segundo item em branco na lista
        self.get_item_input_box().send_keys(Keys.ENTER)
        # Ela recebe um aviso semelhante na página da lista
        self.wait_for_row_in_list_table('1: Compre Leite')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # E ela pode corrigir isso preenchendo o item com um texto
        self.get_item_input_box().send_keys('Fazer chá')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Compre Leite')
        self.wait_for_row_in_list_table('2: Fazer chá')

    def test_cannot_add_duplicate_items(self):
        # Edith acessa a pagina inicial e começa uma nova lista
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Comprar mariolas')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Comprar mariolas')

        # Ela tenta acidentalmente inserir um item duplicado
        self.get_item_input_box().send_keys('Comprar mariolas')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Ela vê uma mensagem de erro
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "Você já inseriu esse item na sua lista."
        ))

    def test_error_message_are_clear_on_input(self):
        # Edna inicia uma lista e provoca um erro de validação
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Fazer massa de pão.')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Fazer massa de pão.')
        self.get_item_input_box().send_keys('Fazer massa de pão.')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))
        # Ela come a digitar na caixa para limpar o erro
        self.get_item_input_box().send_keys('a')

        # Ela fica satisfeita ao ver que a mensagem de erro desaparece
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))   