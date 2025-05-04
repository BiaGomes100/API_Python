import unittest
from flask import Flask,json, make_response,jsonify,request 

app = Flask(__name__)

class TesteTurmas(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def teste_get(self):
        resposta = self.app.get('/Turma/BuscarTurma')
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertIsInstance(data, list)

    def teste_get_por_ID(self):
        resposta = self.app.get('/Turma/BuscarTurmaPorID')
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertIsInstance(data, list)


    def testeAdicionar(self):
        turma = {
            "nome": "Turma A",
            "codigo": "T001"
        }
        resposta = self.app.post('/Turma/AdicionarTurma', json=turma)
        self.assertEqual(resposta.status_code, 201)
        data = json.loads(resposta.data)
        self.assertEqual(data['nome'], "Turma A")
        self.assertEqual(data['codigo'], "T001")

    def testeAtualizar(self):
        turma = {
            "nome": "Turma B",
            "codigo": "T002"
        }
        resposta = self.app.post('/Turma/AtualizarTurma/<int:id>', json=turma)
        turma_id = json.loads(resposta.data)["id"]
        
        updated_data = {
            "nome": "Turma B Atualizada",
            "codigo": "T003"
        }
        resposta = self.app.put(f'/turma/{turma_id}', json=updated_data)
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertEqual(data["nome"], "Turma B Atualizada")
        self.assertEqual(data["codigo"], "T003")

    def testeDeletar_por_ID(self):
        turma = {
            "nome": "Turma C",
            "codigo": "T004"
        }
        resposta = self.app.post('/Turma/DeletarTurmaPorID', json=turma)
        turma_id = json.loads(resposta.data)["id"]

        resposta = self.app.delete(f'/turma/{turma_id}')
        self.assertEqual(resposta.status_code, 200)
        data = json.loads(resposta.data)
        self.assertEqual(data['mensagem'], "Turma removida")



if __name__ == '__main__':
    unittest.main(debug=True)
