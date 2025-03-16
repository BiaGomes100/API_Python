# serve para o python entender que API_PYTHON é o diretorio raiz do projeto fazendo ele identificar mais facil as pastas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask, make_response,jsonify,request ##importando o Flask
from Models.Alunos import *

app = Flask(__name__) ##instanciando o Flask para poder ser usado
app.config['JSON_SORT_KEYS']= False #faz com que não ordene o respose de AaZ



@app.route('/Alunos/BuscarAluno', methods=['GET'])  ##decorator serve para dar uma funcionalidade para a função abaixo, essa por exemplo serve para inicializar a função
def buscarAluno():
    return make_response( 
        jsonify(
            mensagem = 'Lista de alunos',
            dados = Lista_Alunos
            ) #transforma em json bonitinho
    )

@app.route('/Alunos/AdicionarAluno', methods=['POST'])
def adicionar_Aluno():
    aluno = request.json
    Lista_Alunos.append(aluno)
    return make_response(
        jsonify(
            mensagem = 'Aluno cadastrado com sucesso!',
            dado = aluno
            )
        )

@app.route('/Alunos/DeletarAlunoPorID', methods=['DELETE'])
def deletar_aluno():
    alunoParaDeletar = request.json
    
    for aluno in Lista_Alunos:
        if aluno["id"] == alunoParaDeletar["id"]:
            Lista_Alunos.remove(aluno)
            return make_response(
                jsonify(
                    mensagem='Aluno excluído com sucesso!',
                    dado=aluno
                )
            )
        return make_response(jsonify(mensagem='Aluno não encontrado!'), 404)

            

    


app.run()