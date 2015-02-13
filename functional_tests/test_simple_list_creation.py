from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrive_it_later(self):
        # Maria ouviu falar sobre um app de listas bacana.
        # Ela dá uma olhada na homepage do projeto
        self.browser.get(self.server_url)

        # Ela nota que o título da página e o cabeçalho
        # citam to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ela é convidada a inserir, de maneira intuitiva,
        # uma nova tarefa.
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ela digita "Comprar feijão" em uma caixa de texto
        inputbox.send_keys('Comprar feijão')

        # Quando ela aperta Enter, a página é atualizada, e agora,
        # A lista aparece da seguinte forma:
        # "1: comprar feijão" (primeiro item da lista)
        inputbox.send_keys(Keys.ENTER)
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Comprar feijão')

        # Ainda há uma caixa de texto convidando-a para adicionar
        # outro item. Ela insere "Cozinhar o feijão"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Cozinhar o feijão')
        inputbox.send_keys(Keys.ENTER)

        # A página atualiza novamente, e agora mostra os dois
        # items em sua lista
        self.check_for_row_in_list_table('1: Comprar feijão')
        self.check_for_row_in_list_table('2: Cozinhar o feijão')

        # Um novo usuário, João, dá uma olhada no site.

        ## Vamos utilizar uma nova sessão no navegador para ter
        ## certeza que nenhuma informação da Maria apareça para
        ## o João
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # João visita a home page. Não há nenhum sinal da lista da
        # Maria
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar feijão', page_text)
        self.assertNotIn('Cozinhar o feijão', page_text)

        # João começa uma nova lista adicionando um novo item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)

        # João pega sua URL única
        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEqual(joao_list_url, maria_list_url)

        # Novamente, não há nenhum traço da lista da Maria
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comprar feijão', page_text)
        self.assertNotIn('Cozinhar o feijão', page_text)
        self.assertIn('Comprar leite', page_text)
