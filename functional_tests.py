from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicity_wait(3)

    def test_can_start_a_list_and_retrive_it_later(self):
        # Maria ouviu falar sobre um app de listas bacana.
        # Ela dá uma olhada na homepage do projeto
        self.browser.get('http://localhost:8000')

        # Ela nota que o título da página e o cabeçalho
        # citam to-do lists
        self.assertIn('To-Do', browser.title)
        self.fail('Finished the test')

        # Ela é convidada a inserir, de maneira intuitiva,  
        # uma nova tarefa.

        # Ela digita "Comprar feijão" em uma caixa de texto

        # Quando ela aperta Enter, a página é atualizada, e agora,
        # A lista aparece da seguinte forma:
        # "1: comprar feijão" (primeiro item da lista)
        
        # Ainda há uma caixa de texto convidando-a para adicionar
        # outro item. Ela insere "Cozinhar o feijão"

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
