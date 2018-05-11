from selenium import webdriver
from .base import FunctionalTest


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
        self.add_list_item('Procure ajuda')

        # Ela ve uma opção de compartilhe
        share_box = self.browser.find_element_by_css_selector('input[name="share"]')

        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'seu-amigo@exemplo.com'
        )