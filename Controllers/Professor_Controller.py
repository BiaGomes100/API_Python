# serve para o python entender que API_PYTHON é o diretorio raiz do projeto fazendo ele identificar mais facil as pastas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from Models.Professores import *

app = Flask(__name__)


@app.route("/professor/BuscarProfessor", methods=["GET"])
def get_professores():
    return jsonify(ListaProfessores), 200

@app.route("/professor/AdicionarProfessor", methods=["POST"])
def add_professor():
    professor = request.json
    professor["id"] = len(ListaProfessores) + 1
    ListaProfessores.append(professor)
    return jsonify(professor), 201

@app.route("/professor/AtualizarProfessorPorID/<int:id>", methods=["PUT"])
def update_professor(id):
    for professor in ListaProfessores:
        if professor["id"] == id:
            dados = request.json
            professor["nome_do_Professor"] = dados.get("nome_do_Professor", professor["nome_do_Professor"])
            professor["Disciplina"] = dados.get("Disciplina", professor["Disciplina"])
            professor["turma"] = dados.get("turma", professor["turma"])
            return jsonify(professor), 200
    return jsonify({"erro": "Professor não encontrado"}), 404

@app.route("/professor/DeletarProfessorPorID/<int:id>", methods=["DELETE"])
def delete_professor(id):
    for i, professor in enumerate(ListaProfessores):
        if professor["id"] == id:
            del ListaProfessores[i]
            return jsonify({"mensagem": "Professor removido"}), 200
    return jsonify({"erro": "Professor não encontrado"}), 404

app.run(debug=True)