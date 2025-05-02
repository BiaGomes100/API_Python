import requests 
import unittest
from  config import db

class TestStringMethods(unittest.TestCase):


    def test_000_alunos_retorna_lista(self):
        
        r = requests.get('http://127.0.0.1:8000/api/alunos')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        #criar dois alunos (usando post na url /alunos)
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'fernando','id':1})
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'roberto','id':2})
        
        #pego a lista de alunos (do mesmo jeito que no teste 0)
        r_lista = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu
                                        #e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei 
        #aparecem
        achei_fernando = False
        achei_roberto = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_aluno_por_id(self):
        #cria um aluno 'mario', com id 20
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'mario','id':20})

        #consulta a url /alunos/20, pra ver se o aluno está lá
        resposta = requests.get('http://127.0.0.1:8000/api/alunos/20')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'mario') # no dic, o nome tem que ser o 
                                                   # que eu mandei
                                                   # tem que ser mario


    #adiciona um aluno, mas depois reseta o servidor
    #e o aluno deve desaparecer
    def test_003_reseta(self):
        #criei um aluno, com post
        r = requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'cicero','id':29})
        #peguei a lista
        r_lista = requests.get('http://127.0.0.1:8000/api/alunos')
        #no momento, a lista tem que ter mais de um aluno
        self.assertTrue(len(r_lista.json()) > 0)

        #POST na url reseta: deveria apagar todos os dados do servidor
        r_reset = requests.post('http://127.0.0.1:8000/api/alunos/reseta')

        #estou verificando se a url reseta deu pau
        #se voce ainda nao definiu ela, esse cod status nao vai ser 200
        self.assertEqual(r_reset.status_code,200)

        #pego de novo a lista
        r_lista_depois = requests.get('http://127.0.0.1:8000/api/alunos')
        
        #e agora tem que ter 0 elementos
        self.assertEqual(len(r_lista_depois.json()),0)

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
        #apago tudo
        r_reset = requests.post('http://127.0.0.1:8000/api/alunos/reseta')
        self.assertEqual(r_reset.status_code,200)
        #crio 3 alunos
        requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'cicero','id':29})
        requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'lucas','id':28})
        requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'marta','id':27})
        #pego a lista completa
        r_lista = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada = r_lista.json()
        #a lista completa tem que ter 3 elementos
        self.assertEqual(len(lista_retornada),3)
        #faço um request com delete, pra deletar o aluno de id 28
        requests.delete('http://127.0.0.1:8000/api/alunos/28')
        #pego a lista de novo
        r_lista2 = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada2 = r_lista2.json()
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada2),2) 

        acheiMarta = False
        acheiCicero = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'marta':
                acheiMarta=True
            if aluno['nome'] == 'cicero':
                acheiCicero=True
        if not acheiMarta or not acheiCicero:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://127.0.0.1:8000/api/alunos/27')

        r_lista3 = requests.get('http://127.0.0.1:8000/api/alunos')
        lista_retornada3 = r_lista3.json()
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")


    #cria um usuário, depois usa o verbo PUT
    #para alterar o nome do usuário
    def test_005_edita(self):
        #resetei
        r_reset = requests.post('http://127.0.0.1:8000/api/alunos/reseta')
        #verifiquei se o reset foi
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno
        requests.post('http://127.0.0.1:8000/api/alunos',json={'nome':'lucas','id':28})
        #e peguei o dicionario dele
        r_antes = requests.get('http://127.0.0.1:8000/api/alunos/28')
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        #vou editar. Vou mandar um novo dicionario p/ corrigir o dicionario
        #que já estava no 28 (note que só mandei o nome)
        #para isso, uso o verbo PUT
        requests.put('http://127.0.0.1:8000/api/alunos/28', json={'nome':'lucas mendes'})
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://127.0.0.1:8000/api/alunos/28')
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')
        #mas o id nao mudou
        self.assertEqual(r_depois.json()['id'],28)
        
        
        #Testes Professores
    def test_006_professores_retorna_lista(self):
        r = requests.get('http://127.0.0.1:8000/api/professores')
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /professores no seu servidor")
        
        try:
            obj_retornado = r.json()
        except:
            self.fail("Esperava um JSON, mas o servidor retornou outra coisa")
        
        self.assertEqual(type(obj_retornado), type([]))
    
    def test_007_professor_por_id(self):
        r = requests.get('http://127.0.0.1:8000/api/professores/1')
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /professores/<id> no seu servidor")
        
        try:
            obj_retornado = r.json()
        except:
            self.fail("Esperava um JSON, mas o servidor retornou outra coisa")
        
        self.assertIn("nome_do_Professor", obj_retornado)
    
    def test_008_adicionar_professor(self):
        novo_professor = {
            "id": 3,
            "nome_do_Professor": "Ana Lima",
            "turma": "1C",
            "Disciplina": "Matemática"
        }
        r = requests.post('http://127.0.0.1:8000/api/professores', json=novo_professor)
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /professores no seu servidor")
        
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["nome_do_Professor"], "Ana Lima")
    
    def test_009_atualizar_professor(self):
        atualizacao = {"Disciplina": "Química"}
        r = requests.put('http://127.0.0.1:8000/api/professores/1', json=atualizacao)
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /professores/<id> no seu servidor")
        
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["Disciplina"], "Química")
    
    def test_010_excluir_professor(self):
        r = requests.delete('http://127.0.0.1:8000/api/professores/2')
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /professores/<id> no seu servidor")
        
        self.assertEqual(r.status_code, 204)
        
        r_check = requests.get('http://127.0.0.1:8000/api/professores/2')
        self.assertEqual(r_check.status_code, 404)
    
    
    #TESTES TURMA
    
    def test_011_turmas_retorna_lista(self):
        r = requests.get('http://127.0.0.1:8000/api/turma')
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /turma no seu servidor")
        
        try:
            obj_retornado = r.json()
        except:
            self.fail("Esperava um JSON, mas o servidor retornou outra coisa")
        
        self.assertEqual(type(obj_retornado), type([]))
    
    def test_012_turma_por_id(self):
        r = requests.get('http://127.0.0.1:8000/api/turma/1')
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /turma/<id> no seu servidor")
        
        try:
            obj_retornado = r.json()
        except:
            self.fail("Esperava um JSON, mas o servidor retornou outra coisa")
        
        self.assertIn("numero_turma", obj_retornado)
    
    def test_013_adicionar_turma(self):
        nova_turma = {
            "id": 3,
            "quantidade_alunos": 28,
            "numero_turma": "2C",
            "professor_representante": "Ana Lima"
        }
        r = requests.post('http://127.0.0.1:8000/api/turma', json=nova_turma)
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /turma no seu servidor")
        
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["numero_turma"], "2C")
    
    def test_014_atualizar_turma(self):
        atualizacao = {"quantidade_alunos": 35}
        r = requests.put('http://127.0.0.1:8000/api/turma/1', json=atualizacao)
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /turma/<id> no seu servidor")
        
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["quantidade_alunos"], 35)
    
    def test_015_excluir_turma(self):
        r = requests.delete('http://127.0.0.1:8000/api/turma/2')
        
        if r.status_code == 404:
            self.fail("Você não definiu a página /turma/<id> no seu servidor")
        
        self.assertEqual(r.status_code, 204)
        
        r_check = requests.get('http://127.0.0.1:8000/api/turma/2')
        self.assertEqual(r_check.status_code, 404)

   



def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()