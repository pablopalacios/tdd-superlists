from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Maria vai para a página inicial e acidentalmente submete
        # uma lista vazia. Ela aperta enter com a caixa vazia
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # A página atualiza e há uma mensagem de erro dizendo que
        # uma lista não pode ser iniciada com itens em branco
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # Ela tenta novamente com algum texto para um item, o que faz
        # funcionar agora
        self.get_item_input_box().send_keys('Comprar leite\n')
        self.check_for_row_in_list_table('1: Comprar leite')

        # Perversa, ela tenta submeter mais um item em branco na lista
        self.get_item_input_box().send_keys('\n')

        # Ela recebe uma mensagem similar na página da lista
        self.check_for_row_in_list_table('1: Comprar leite')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # E ela corrige seu erro colocando algum texto no input
        self.get_item_input_box().send_keys('Fazer chá\n')
        self.check_for_row_in_list_table('1: Comprar leite')
        self.check_for_row_in_list_table('2: Fazer chá')

    def test_cannot_add_duplicate_items(self):
        # Maria vai para a páfina inicial e começa uma nova lista
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Comprar ameixas\n')
        self.check_for_row_in_list_table('1: Comprar ameixas')

        # Ela tenta, acidentalmente, inserir um item já inserido
        self.get_item_input_box().send_keys('Comprar ameixas\n')

        # Ela vê uma mensagem de erro bem auxiliadora
        self.check_for_row_in_list_table('1: Comprar ameixas')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # Maria inicia uma nova lista de uma maneira que causa um erro de validação
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # Ela começa a digitar na caixa de entrada para limpar o erro
        self.get_item_input_box().send_keys('a')

        # Ela fica maravilhada em ver que a mensagem de erro desapareceu
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
