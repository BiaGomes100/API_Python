import sys
import os
from flask import Flask, make_response, jsonify, request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importando modelo
from Models.Alunos import Lista_Alunos

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Impede a ordenação automática da resposta JSON


@app.route('/Alunos/BuscarAluno', methods=['GET'])
def buscarAluno():
    try:
        return make_response(
            jsonify(
                mensagem='Lista de alunos',
                dados=Lista_Alunos
            ), 200
        )
    except Exception as e:
        return make_response(jsonify(erro=str(e)), 500)


@app.route('/Alunos/AdicionarAluno', methods=['POST'])
def adicionar_Aluno():
    try:
        aluno = request.json

        # Verifica se os campos essenciais existem
        if not aluno or 'id' not in aluno or 'nome' not in aluno:
            return make_response(jsonify(mensagem="Dados inválidos. O JSON deve conter 'id' e 'nome'."), 400)

        # Verifica se o ID já existe
        if any(a["id"] == aluno["id"] for a in Lista_Alunos):
            return make_response(jsonify(mensagem="Já existe um aluno com esse ID!"), 409)

        Lista_Alunos.append(aluno)
        return make_response(
            jsonify(
                mensagem='Aluno cadastrado com sucesso!',
                dado=aluno
            ), 201
        )

    except Exception as e:
        return make_response(jsonify(erro=str(e)), 500)


@app.route('/Alunos/DeletarAlunoPorID', methods=['DELETE'])
def deletar_aluno():
    try:
        alunoParaDeletar = request.json

        if not alunoParaDeletar or 'id' not in alunoParaDeletar:
            return make_response(jsonify(mensagem="O JSON deve conter o campo 'id'."), 400)

        for aluno in Lista_Alunos:
            if aluno["id"] == alunoParaDeletar["id"]:
                Lista_Alunos.remove(aluno)
                return make_response(
                    jsonify(
                        mensagem='Aluno excluído com sucesso!',
                        dado=aluno
                    ), 200
                )

        return make_response(jsonify(mensagem='Aluno não encontrado!'), 404)

    except Exception as e:
        return make_response(jsonify(erro=str(e)), 500)


if __name__ == '__main__':
    app.run()
