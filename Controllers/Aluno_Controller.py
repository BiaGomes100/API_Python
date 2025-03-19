import sys
import os
from flask import Flask, make_response, jsonify, request

# Serve para o Python entender que API_PYTHON é o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importando a lista de alunos (Certifique-se de que essa variável 'Lista_Alunos' está definida)
from Models.Alunos import Lista_Alunos

app = Flask(__name__)  # Instanciando o Flask para poder ser usado
app.config['JSON_SORT_KEYS'] = False  # Faz com que não ordene o response de A-Z


# Rota para buscar todos os alunos
@app.route('/Alunos/BuscarAluno', methods=['GET'])
def buscarAluno():
    return make_response(
        jsonify(
            mensagem='Lista de alunos',
            dados=Lista_Alunos
        )
    )


# Rota para adicionar um aluno
@app.route('/Alunos/AdicionarAluno', methods=['POST'])
def adicionar_Aluno():
    aluno = request.json  # Recebendo o aluno no formato JSON
    Lista_Alunos.append(aluno)  # Adicionando o aluno à lista
    return make_response(
        jsonify(
            mensagem='Aluno cadastrado com sucesso!',
            dado=aluno
        )
    )


# Rota para deletar aluno por ID
@app.route('/Alunos/DeletarAlunoPorID', methods=['DELETE'])
def deletar_aluno():
    alunoParaDeletar = request.json  # Recebendo o ID do aluno a ser deletado
    
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


if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Definindo a porta 5002 para rodar a API
