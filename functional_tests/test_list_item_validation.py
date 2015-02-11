from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Maria vai para a página inicial e acidentalmente submete
        # uma lista vazia. Ela aperta enter com a caixa vazia
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # A página atualiza e há uma mensagem de erro dizendo que
        # uma lista não pode ser iniciada com itens em branco
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # Ela tenta novamente com algum texto para um item, o que faz
        # funcionar agora
        self.browser.find_element_by_id('id_new_item').send_keys('Comprar leite\n')
        self.check_for_row_in_list_table('1: Comprar leite')

        # Perversa, ela tenta submeter mais um item em branco na lista
        self.browser.find_element_by_id('id_new_item').send_keys('Comprar leite\n')

        # Ela recebe uma mensagem similar na página da lista
        self.check_for_row_in_list_table('1: Comprar leite')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # E ela corrige seu erro colocando algum texto no input
        self.browser.find_element_by_id('id_new_item').send_keys('Fazer chá\n')
        self.check_for_row_in_list_table('1: Comprar leite')
        self.check_for_row_in_list_table('2: Fazer chá')
