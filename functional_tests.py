from selenium import webdriver
import unittest


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
        self.assertIn('To-do', self.browser.title)
        self.fail('Teste finalizado!')

        # Ele é convidado a inserir um item de tarefa

        # Ele digita "Comprar penas de pavão" em uma caixa de texto

        # Quando ele aperta enter, a pagina é atualizada e agora a pagina lista
        # 1: Comprar penas de pavão como um item em uma lista de tarefas

        # Ainda há uma caixa de texto e ele acrescenta "Fazer isca de pesca"

        #  A página é atualizada novamente e agora mostra dois itens na lista

        # João se pergunta se o site irá lembrar dessa lista. Então ele percebe que o site gerou um
        # url único para ele - há um texto explicando isso

        # Ele acessa a url e verifica que sua lista continua lá

        # Satisfeito ele vai durmir


def main():
    unittest.main(warnings='ignore')


if __name__ == '__main__':
    main()
