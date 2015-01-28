from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def test_can_start_a_list_and_retrive_it_later(self):
        # Maria ouviu falar sobre um app de listas bacana.
        # Ela dá uma olhada na homepage do projeto
        self.browser.get('http://localhost:8000')

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Comprar feijão' for row in rows),
            "New to-do item did not appear in table"
        )
        
        # Ainda há uma caixa de texto convidando-a para adicionar
        # outro item. Ela insere "Cozinhar o feijão"
        self.fail('Finish the test!')

        # A página atualiza novamente, e agora mostra os dois 
        # items em sua lista

        # Maria pensa como o site irá lembrar da sua lista. Aí,
        # ela vê que o site criou uma URL única para ela -- há
        # algum texto explicativo para isso.


        # Ela vista a URL - sua lista de tarefas ainda está lá.

    def tearDown(self):
        # Satisfeita, ela desliga o computador.
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
