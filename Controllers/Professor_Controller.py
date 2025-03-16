from flask import Flask, jsonify, request

app = Flask(__name__)

ListaProfessores = []

@app.route("/professor", methods=["GET"])
def get_professores():
    return jsonify(ListaProfessores), 200

@app.route("/professor", methods=["POST"])
def add_professor():
    professor = request.json
    professor["id"] = len(ListaProfessores) + 1
    ListaProfessores.append(professor)
    return jsonify(professor), 201

@app.route("/professor/<int:id>", methods=["PUT"])
def update_professor(id):
    for professor in ListaProfessores:
        if professor["id"] == id:
            dados = request.json
            professor["nome"] = dados.get("nome", professor["nome"])
            professor["disciplina"] = dados.get("disciplina", professor["disciplina"])
            return jsonify(professor), 200
    return jsonify({"erro": "Professor não encontrado"}), 404
        #alguem pode verificar? me perdi fazendo esse e só consegui com o chat 

@app.route("/professor/<int:id>", methods=["DELETE"])
def delete_professor(id):
    for i, professor in enumerate(ListaProfessores):
        if professor["id"] == id:
            del ListaProfessores[i]
            return jsonify({"mensagem": "Professor removido"}), 200
    return jsonify({"erro": "Professor não encontrado"}), 404

app.run(debug=True)
