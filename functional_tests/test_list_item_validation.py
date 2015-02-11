from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Maria vai para a página inicial e acidentalmente submete
        # uma lista vazia. Ela aperta enter com a caixa vazia

        # A página atualiza e há uma mensagem de erro dizendo que
        # uma lista não pode ser iniciada com itens em branco

        # Ela tenta novamente com algum texto para um item, o que faz
        # funcionar agora

        # Perversa, ela tenta submeter mais um item em branco na lista

        # Ela recebe uma mensagem similar na página da lista

        # E ela corrige seu erro colocando algum texto no input
        self.fail('write me')
