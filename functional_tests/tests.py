import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        """
        Abre um navegador para cada teste e espera por 3
        segundos antes de fazer qualquer coisa. Selenium pode
        começar a processar algo antes que a página seja carregada,
        possibilitando que alguns testes falhem inesperadamente.
        """
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def check_for_row_in_list_table(self, row_text):
        """ Função auxiliar para verificar se um determinado
        texto se encontra em uma tabela HTML """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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
        inputbox = self.browser.find_element_by_id('id_new_item')
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
        inputbox = self.browser.find_element_by_id('id_new_item')
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
        inputbox = self.browser.find_element_by_id('id_new_item')
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

    def test_layout_and_styling(self):
        # Maria vai para a home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Ela nota que o botão de input está centralizado
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # Ela começa uma nova lista e vê que tudo está centralizado
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

    def tearDown(self):
        # Satisfeitos, ambos vão dormir
        self.browser.quit()
