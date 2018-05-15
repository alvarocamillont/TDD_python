from selenium import webdriver

from .base import FunctionalTest
from .list_page import ListPage
from .my_list_page import MyListPage



def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Judite é uma usuaria logada
        self.create_pre_authenticated_session('judite@exemplo.com')
        judite_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(judite_browser))

        # seu amigo Pedro também está no site de listas
        pedro_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(pedro_browser))
        self.browser = pedro_browser
        self.create_pre_authenticated_session('pedro@example.com')

        # Judite acessa a página inicial e começa uma lista
        self.browser = judite_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Procure ajuda')

        # Ela ve uma opção de compartilhe
        share_box = list_page.get_share_box()

        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'seu-amigo@exemplo.com'
        )

        # Ela compatilha a lista 
        # A pagina é atualizada informando que a lista foi compartilhada
        # com o pedro

        list_page.share_list_with('pedro@example.com')

        # Pedro agora acessa a página de listas com o seu navegador
        self.browser = pedro_browser
        MyListPage(self).go_to_my_lists_page()

        # Ele ve ai a lista de Judite
        self.browser.find_element_by_link_text('Procure ajuda').click()

        # Na página de lista, Pedro pode ver que a lista é de Judite
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'judite@exemplo.com'
        ))

        # Ele adiciona um item na lista
        list_page.add_list_item('Olá Judite!')

        # Quando Judite atualiza a página, ela vê o acrécimo feito por pedro
        self.browser = judite_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Olá Judite!', 2)
        
