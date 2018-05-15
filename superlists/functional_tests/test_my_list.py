
from .base import FunctionalTest


class MyListTest(FunctionalTest):

    def test_logged_in_users_list_are_saved_as_my_lists(self):
        email = 'judite@exemplo.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Judite é uma usuária logada
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_user_lists_are_saved_as_my_lists(self):
        # Judite é uma usuaria logada
        self.create_pre_authenticated_session('judite@exemplo.com.br')

        # Judite acessa apágina inicial e começa uma lista
        self.browser.get(self.live_server_url)
        self.add_list_item('Nintendo Switch')
        self.add_list_item('Playstation 4')
        firt_list_url = self.browser.current_url

        # Ela percebe o link para Mylist pela primeira vez
        self.browser.find_element_by_link_text('Minhas Listas').click()

        # Ela ve que sua lista está lá, nomeada de acordo com
        # O primeiro item da lista
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Nintendo Switch')
        )
        self.browser.find_element_by_link_text('Nintendo Switch').click()

        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, firt_list_url)
        )

        # Ela decide comecar uma nova lista
        self.browser.get(self.live_server_url)
        self.add_list_item('Clique teste')

        second_list_url = self.browser.current_url

        # Em Minhas Lista a sua nova lista aparece
        self.browser.find_element_by_link_text('Minhas Listas').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Clique teste')
        )
        self.browser.find_element_by_link_text('Clique teste').click()

        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Ela faz logout e a opção My List desparece
        self.browser.find_element_by_link_text('Log Out').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_elements_by_link_text('Minhas Listas'), []))
