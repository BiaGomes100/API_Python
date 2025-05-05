import requests 
import unittest

class TestStringMethods(unittest.TestCase):


    def test_000_alunos_retorna_lista(self):
        
        r = requests.get('http://127.0.0.1:8000/api/alunos')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail('voce nao definiu a pagina /alunos no seu server')

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail('queria um json mas voce retornou outra coisa')

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        #criar dois alunos (usando post na url /alunos)
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome_Aluno':'fernando', 'data_nascimento':'2005-03-15', 'email':'fernando123@teste.com', 'telefone':'87654321'})
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome_Aluno':'roberto','data_nascimento':'2005-03-15', 'email':'robert123o@teste.com', 'telefone':'87654322'})
        
        #pego a lista de alunos (do mesmo jeito que no teste 0)
        r_lista = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu
                                        #e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei 
        #aparecem
        achei_fernando = False
        achei_roberto = False
        for aluno in lista_retornada:
            if aluno['nome_Aluno'] == 'fernando':
                achei_fernando = True
            if aluno['nome_Aluno'] == 'roberto':
                achei_roberto = True
        
        #se algum desses 'achei' nao for True, dou uma falha
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        #cria um aluno 'mario', com id 20
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome_Aluno':'bia','data_nascimento':'2005-03-15', 'email':'1213sadasdsa@teste.com', 'telefone':'87654323'})

         # captura o ID do aluno criado
        aluno_criado = r.json()
        self.assertIn('body', aluno_criado[0])  # verifica se o campo 'body' está presente
        id_criado = aluno_criado[0]['body']  # pega o ID do aluno criado


        #consulta a url /alunos/20, pra ver se o aluno está lá
        resposta = requests.get(f'http://127.0.0.1:8000/api/alunos/{id_criado}')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome_Aluno',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome_Aluno
        self.assertEqual(dict_retornado['nome_Aluno'],'bia') # no dic, o nome_Aluno tem que ser o 
                                                   # que eu mandei
                                                   # tem que ser bia
     
    #adiciona um aluno, mas depois reseta o servidor
    #e o aluno deve desaparecer
    def test_003_reseta(self):
    # Cria um aluno
        r = requests.post('http://127.0.0.1:8000/api/alunos', json={
            'nome_Aluno': 'cicero',
            'data_nascimento': '2005-03-15',
            'email': 'cicerow@teste.com',
            'telefone': '87654324'
        }) 
        self.assertEqual(r.status_code, 201)

        # Pega a lista de alunos
        r_lista = requests.get('http://127.0.0.1:8000/api/alunos')
        self.assertTrue(len(r_lista.json()) > 0)

        # POST na URL reseta: deveria apagar todos os dados do servidor
        r_reset = requests.post('http://127.0.0.1:8000/api/alunos/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Pega de novo a lista
        r_lista_depois = requests.get('http://127.0.0.1:8000/api/alunos')
        self.assertEqual(len(r_lista_depois.json()), 0)

    #esse teste adiciona 2 alunos, depois deleta 1
    #e verifica que o numero de alunos realmente diminuiu
    '''
    voce provavelmente vai querer usar o lista.remove
    >>> lista
    [10, 20, 'banana']
    >>> lista.remove('banana')
    >>> lista
    [10, 20]
    >>> lista.remove(10)
    >>> lista
    [20]'''
    def test_004_deleta(self):
        # Apago tudo
        r_reset = requests.post('http://127.0.0.1:8000/api/alunos/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Crio 3 alunos
        r1 = requests.post('http://127.0.0.1:8000/api/alunos', json={
            'nome_Aluno': 'cicero',
            'data_nascimento': '2005-03-15',
            'email': 'cicero@teste.com',
            'telefone': '123456789'
        })
        r2 = requests.post('http://127.0.0.1:8000/api/alunos', json={
            'nome_Aluno': 'lucas',
            'data_nascimento': '2005-03-15',
            'email': 'lucas@teste.com',
            'telefone': '123456788'
        })
        r3 = requests.post('http://127.0.0.1:8000/api/alunos', json={
            'nome_Aluno': 'marta',
            'data_nascimento': '2005-03-15',
            'email': 'marta@teste.com',
            'telefone': '123456787'
        })
        self.assertEqual(r1.status_code, 201)
        self.assertEqual(r2.status_code, 201)
        self.assertEqual(r3.status_code, 201)

        # Pego a lista completa
        r_lista = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada = r_lista.json()
        self.assertEqual(len(lista_retornada), 3)

        # Faço um request com DELETE para deletar o aluno de ID 2
        id_lucas = lista_retornada[1]['id']
        requests.delete(f'http://127.0.0.1:8000/api/alunos/{id_lucas}')

        # Pego a lista de novo
        r_lista2 = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada2 = r_lista2.json()
        self.assertEqual(len(lista_retornada2), 2)

        # Verifico se os alunos restantes são os corretos
        nome_Alunos_restantes = [aluno['nome_Aluno'] for aluno in lista_retornada2]
        self.assertIn('cicero', nome_Alunos_restantes)
        self.assertIn('marta', nome_Alunos_restantes)

    #cria um usuário, depois usa o verbo PUT
    #para alterar o nome_Aluno do usuário
    def test_005_edita(self):
        #resetei
        r_reset = requests.post('http://127.0.0.1:8000/api/alunos/reseta')
        #verifiquei se o reset foi
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome_Aluno':'fernando', 'data_nascimento':'2005-03-15', 'email':'fernando@teste.com', 'telefone':'87654321'})
        #e peguei o dicionario dele

        aluno_criado = r.json()
        self.assertIn('body', aluno_criado[0])  # verifica se o campo 'body' está presente
        id_criado = aluno_criado[0]['body']  # pega o ID do aluno criado

        r_antes = requests.get(f'http://127.0.0.1:8000/api/alunos/{id_criado}')
        #o nome_Aluno enviado foi lucas, o nome_Aluno recebido tb
        self.assertEqual(r_antes.json()['nome_Aluno'],'fernando')
        #vou editar. Vou mandar um novo dicionario p/ corrigir o dicionario
        #para isso, uso o verbo PUT
        requests.put(f'http://127.0.0.1:8000/api/alunos/{id_criado}', json={'nome_Aluno':'bia','data_nascimento':'2005-03-15', 'email':'biadsgsdk@teste.com', 'telefone':'87654323'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get(f'http://127.0.0.1:8000/api/alunos/{id_criado}')
        #agora o nome_Aluno deve ser lucas mendes
        self.assertEqual(r_depois.json()['nome_Aluno'],'bia')
        #mas o id nao mudou
        self.assertEqual(r_depois.json()['id'],id_criado)
        
        
        #Testes Professores
    def test_006_professores_retorna_lista(self):
        r = requests.get('http://127.0.0.1:8000/api/professores')
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /professores no seu servidor')
        
        try:
            obj_retornado = r.json()
        except:
            self.fail('Esperava um JSON, mas o servidor retornou outra coisa')
        
        self.assertEqual(type(obj_retornado), type([]))
    
    def test_007_professor_por_id(self):
        r = requests.post('http://127.0.0.1:8000/api/professores',json={'nome_professor':'biago','turma':'ADS3c', 'disciplina':'adsss'})

         # captura o ID do professor criado
        professor_criado = r.json()
        self.assertIn('body', professor_criado[0])  # verifica se o campo 'body' está presente
        id_criado = professor_criado[0]['body']
        
        resposta = requests.get(f'http://127.0.0.1:8000/api/professores/{id_criado}')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome_professor',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome_Aluno
        self.assertEqual(dict_retornado['nome_professor'],'biago')

        if r.status_code == 404:
            self.fail('Você não definiu a página /professores/<id> no seu servidor')
        
        try:
            obj_retornado = dict_retornado
        except:
            self.fail('Esperava um JSON, mas o servidor retornou outra coisa')
        
        self.assertIn('nome_professor', obj_retornado)
    
    def test_008_adicionar_professor(self):
        novo_professor = {
            'nome_professor': 'Ana Lima',
            'turma': '1C',
            'disciplina': 'Matemática'
        }
        r = requests.post('http://127.0.0.1:8000/api/professores', json=novo_professor)
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /professores no seu servidor')
        
        self.assertEqual(r.status_code, 201)
        self.assertEqual(novo_professor['nome_professor'], 'Ana Lima')
    
    def test_009_atualizar_professor(self):
        atualizacao = {'disciplina': 'Quimica'}

        r = requests.post('http://127.0.0.1:8000/api/professores',json={'nome_professor':'Cesar','turma':'CCA3', 'disciplina':'ciencias da computação'})

        professor_criado = r.json()
        self.assertIn('body', professor_criado[0])  # verifica se o campo 'body' está presente
        id_criado = professor_criado[0]['body']  # pega o ID do aluno criado

        r_antes = requests.get(f'http://127.0.0.1:8000/api/professores/{id_criado}')
        self.assertEqual(r_antes.json()['nome_professor'],'Cesar')
        requests.put(f'http://127.0.0.1:8000/api/professores/{id_criado}', json=atualizacao)
        r_depois = requests.get(f'http://127.0.0.1:8000/api/professores/{id_criado}')
        self.assertEqual(r_depois.json()['nome_professor'],'Cesar')
        self.assertEqual(r_depois.json()['id'],id_criado)
        
        r = requests.put(f'http://127.0.0.1:8000/api/professores/{id_criado}', json=atualizacao)
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /professores/<id> no seu servidor')
        
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r_depois.json()['disciplina'], 'Quimica')
    
    def test_010_excluir_professor(self):
        r = requests.post('http://127.0.0.1:8000/api/professores',json={'nome_professor':'Marisa','turma':'CCA6', 'disciplina':'ciencias da computação'})

        professor_criado = r.json()
        self.assertIn('body', professor_criado[0])  # verifica se o campo 'body' está presente
        id_criado = professor_criado[0]['body']

        r_antes = requests.get(f'http://127.0.0.1:8000/api/professores/{id_criado}')
        self.assertEqual(r_antes.json()['nome_professor'],'Marisa')

        r = requests.delete(f'http://127.0.0.1:8000/api/professores/{id_criado}')
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /professores/<id> no seu servidor')
        
        self.assertEqual(r.status_code, 204)
        
        r_check = requests.get(f'http://127.0.0.1:8000/api/professores/{id_criado}')
        self.assertEqual(r_check.status_code, 404)
    
    
    #TESTES TURMA
    
    def test_011_turmas_retorna_lista(self):
        r = requests.get('http://127.0.0.1:8000/api/turma')
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /turma no seu servidor')
        
        try:
            obj_retornado = r.json()
        except:
            self.fail('Esperava um JSON, mas o servidor retornou outra coisa')
        
        self.assertEqual(type(obj_retornado), type([]))
    
    def test_012_turma_por_id(self):
        r = requests.post('http://127.0.0.1:8000/api/turma',json={'nome_turma':'BDD','ano':3, 'turno':'MANHA'})

        turma_criado = r.json()
        self.assertIn('body', turma_criado[0])  # verifica se o campo 'body' está presente
        id_criado = turma_criado[0]['body']


        r = requests.get(f'http://127.0.0.1:8000/api/turma/{id_criado}')
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /turma/<id> no seu servidor')
        
        try:
            obj_retornado = r.json()
        except:
            self.fail('Esperava um JSON, mas o servidor retornou outra coisa')
        
        self.assertIn('ano', obj_retornado)
    
    def test_013_adicionar_turma(self):
        nova_turma = {
            'nome_turma': 'AWS',
            'ano': 2,
            'turno':'TARDE'
        }
        r = requests.post('http://127.0.0.1:8000/api/turma', json=nova_turma)
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /turma no seu servidor')
        

        self.assertEqual(r.status_code, 201)
        self.assertEqual(nova_turma['ano'], 2)
    
    def test_014_atualizar_turma(self):
        atualizacao = {'ano': 5}

        r = requests.post('http://127.0.0.1:8000/api/turma',json={'nome_turma':'CLOUD','ano':3, 'turno':'NOITE'})

        turma_criado = r.json()
        self.assertIn('body', turma_criado[0])  # verifica se o campo 'body' está presente
        id_criado = turma_criado[0]['body']

        r_put = requests.put(f'http://127.0.0.1:8000/api/turma/{id_criado}', json=atualizacao)
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /turma/<id> no seu servidor')
        
        self.assertEqual(r_put.status_code, 200)
        self.assertEqual(r_put.json()['ano'], 5)
    
    def test_015_excluir_turma(self):
        r = requests.post('http://127.0.0.1:8000/api/turma',json={'nome_turma':'DEVOPS','ano':2, 'turno':'MANHA'})

        turma_criado = r.json()
        self.assertIn('body', turma_criado[0])  # verifica se o campo 'body' está presente
        id_criado = turma_criado[0]['body']

        r = requests.delete(f'http://127.0.0.1:8000/api/turma/{id_criado}')
        
        if r.status_code == 404:
            self.fail('Você não definiu a página /turma/<id> no seu servidor')
        
        self.assertEqual(r.status_code, 204)
        
        r_check = requests.get(f'http://127.0.0.1:8000/api/turma/{id_criado}')
        self.assertEqual(r_check.status_code, 404)

   



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()