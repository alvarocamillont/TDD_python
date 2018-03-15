from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

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
