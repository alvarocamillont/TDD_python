from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

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
