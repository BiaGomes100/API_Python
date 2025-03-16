import unittest
from flask import Flask, json, make_response,jsonify,request 

app = Flask(__name__)

class TesteProfessores(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def teste_get (self):
        resposta = self.app.get('/professor')
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertIsInstance(data, list)

    def testeAdicionar(self):
        professor = {
            "nome": "Carlos Souza",
            "disciplina": "Matemática"
        }
        resposta = self.app.post('/professor', json=professor)
        self.assertEqual(resposta.status_code, 201)
        data = json.loads(resposta.data)
        self.assertEqual(data['nome'], "Carlos Souza")
        self.assertEqual(data['disciplina'], "Matemática")

    def testeAtualizar(self):
        professor = {
            "nome": "Maria Oliveira",
            "disciplina": "Física"
        }
        resposta = self.app.post('/professor', json=professor)
        professor_id = json.loads(resposta.data)["id"]
        
        updated_data = {
            "nome": "Maria Oliveira",
            "disciplina": "Química"
        }
        resposta = self.app.put(f'/professor/{professor_id}', json=updated_data)
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertEqual(data["disciplina"], "Química")

    def testeDeletar(self):
        professor = {
            "nome": "José Silva",
            "disciplina": "Química"
        }
        resposta = self.app.post('/professor', json=professor)
        professor_id = json.loads(resposta.data)["id"]

        resposta = self.app.delete(f'/professor/{professor_id}')
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertEqual(data['mensagem'], "Professor removido")

    def testeDeletarProfessorNaoEncontrado(self):
        resposta = self.app.delete('/professor/999')
        self.assertEqual(resposta.status_code, 404)
        data = json.loads(resposta.data)
        self.assertEqual(data['erro'], 'Professor não encontrado')


if __name__ == '__main__':
    app.run(debug=True)

