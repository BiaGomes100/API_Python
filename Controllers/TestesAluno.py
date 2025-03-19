import unittest
from flask import Flask, json, make_response,jsonify,request 

app = Flask(__name__)

class Teste(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def teste_get(self):
        resposta = self.app.get('/Alunos/BuscarAluno')
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertIsInstance(data['dados'], list)

    def testeAdicionar(self):
        aluno = {
            "id": 1,
            "nome": "João Silva",
            "idade": 20
        }
        resposta = self.app.post('/Alunos/AdicionarAluno', json=aluno)
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertEqual(data['mensagem'], "Aluno cadastrado com sucesso!")
        self.assertEqual(data['dado']['nome'], "João Silva")
        self.assertEqual(data['dado']['idade'], 20)


    def testeDeletar(self):
        aluno = {
            "id": 2,
            "nome": "Maria Oliveira",
            "idade": 22
        }
        self.app.post('/Alunos/AdicionarAluno', json=aluno)  # Agora o aluno existe

        resposta = self.app.delete('/Alunos/DeletarAlunoPorID', json={"id": 2})
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertEqual(data['mensagem'], 'Aluno excluído com sucesso!')
        self.assertEqual(data['dado']['nome'], "Maria Oliveira")


    def testeDeletarAlunoNaoEncontrado(self):
        resposta = self.app.delete('/Alunos/DeletarAlunoPorID', json={"id": 999})
        self.assertEqual(resposta.status_code, 404)
        data = json.loads(resposta.data)
        self.assertEqual(data['mensagem'], 'Aluno não encontrado!')

    def testeAdicionarAlunoInvalido(self):
        aluno_invalido = {
            "id": "não é um número",  # id inválido
            "nome": "Carlos Souza"
        }
        resposta = self.app.post('/Alunos/AdicionarAluno', json=aluno_invalido)
        self.assertEqual(resposta.status_code, 400)  # Alterado para verificar o erro de validação
        data = json.loads(resposta.data)
        self.assertEqual(data['mensagem'], "ID inválido, deve ser um número inteiro.")


if __name__ == '__main__':
    app.run(debug=True)
















