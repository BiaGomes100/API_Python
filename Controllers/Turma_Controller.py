from flask import Flask, make_response, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

turmas = []

@app.route('/Turma/BuscarTurmaPorID', methods=['GET'])
def buscarTurma_id():
    turmaParaBuscar = request.json
    if not turmaParaBuscar or 'id' not in turmaParaBuscar:
        return make_response(
            jsonify(
                mensagem='Erro: ID não fornecido.',
                dados=None
            ), 400
        )

    id = turmaParaBuscar['id']
    if verificarID(id):
        return make_response(
            jsonify(
                mensagem='Erro: ID vazio.',
                dados=None
            ), 400
        )

    for turma in turmas:
        if turma["id"] == id:
            return make_response(
                jsonify(
                    mensagem='Turma encontrada:',
                    dados=turma
                ), 200
            )

    return make_response(
        jsonify(
            mensagem='Turma não encontrada.',
            dados=None
        ), 404
    )

@app.route('/Turma/BuscarTurmas', methods=['GET'])
def buscarTurmas():
    return make_response(
        jsonify(
            mensagem='Lista de turmas',
            dados=turmas
        ), 200
    )

@app.route('/Turma/AdicionarTurma', methods=['POST'])
def adicionar_turma():
    turma = request.json
    if not validarTurma(turma):
        return make_response(
            jsonify(
                mensagem='Erro: Todos os campos são obrigatórios.',
                dados=None
            ), 400
        )

    for t in turmas:
        if t["id"] == turma["id"]:
            return make_response(
                jsonify(
                    mensagem='Erro: ID já existe.',
                    dados=None
                ), 400
            )

    turmas.append(turma)
    return make_response(
        jsonify(
            mensagem='Turma cadastrada com sucesso!',
            dado=turma
        ), 200
    )

@app.route('/Turma/AtualizarTurma/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    dados_atualizados = request.json
    if not validarTurma(dados_atualizados):
        return make_response(
            jsonify(
                mensagem='Erro: Todos os campos são obrigatórios.',
                dados=None
            ), 400
        )

    for turma in turmas:
        if turma["id"] == id:
            turma.update(dados_atualizados)
            return make_response(
                jsonify(
                    mensagem='Turma atualizada com sucesso!',
                    dados=turma
                ), 200
            )

    return make_response(
        jsonify(
            mensagem='Erro: Turma não encontrada.',
            dados=None
        ), 404
    )

@app.route('/Turma/DeletarTurmaPorID', methods=['DELETE'])
def deletar_turma():
    turmaParaDeletar = request.json
    if not turmaParaDeletar or 'id' not in turmaParaDeletar:
        return make_response(
            jsonify(
                mensagem='Erro: ID não fornecido.',
                dados=None
            ), 400
        )

    id = turmaParaDeletar['id']
    if verificarID(id):
        return make_response(
            jsonify(
                mensagem='Erro: ID vazio.',
                dados=None
            ), 400
        )

    for turma in turmas:
        if turma["id"] == id:
            turmas.remove(turma)
            return make_response(
                jsonify(
                    mensagem='Turma excluído com sucesso!',
                    dado=turma
                ), 200
            )

    return make_response(
        jsonify(
            mensagem='Erro: Turma não encontrada.',
            dados=None
        ), 404
    )

def verificarID(id):
    if id is None:
        return True
    return False

def validarTurma(turma):
    campos_obrigatorios = ["id", "quantidade_alunos", "numero_turma", "professor_representante"]
    for campo in campos_obrigatorios:
        if campo not in turma or turma[campo] in [None, ""]:
            return False
    return True

if __name__ == '__main__':
    app.run(debug=True, port=5000)