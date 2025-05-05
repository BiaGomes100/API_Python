from flask import Blueprint, request, jsonify
from Models.Turmas import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turma_blueprint = Blueprint('turma', __name__)

@turma_blueprint.route('/turma', methods=['GET'])
def get_turmas():
    return jsonify(listar_turmas())

@turma_blueprint.route('/turma/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma= turma_por_id(id_turma)
        return jsonify(turma)
    except TurmaNaoEncontrada:
        return jsonify({'message': 'turma não encontrada'}), 404

@turma_blueprint.route('/turma', methods=['POST'])
def create_turma():
    data = request.json
    response = adicionar_turma(data)
    return jsonify(response), 201

@turma_blueprint.route('/turma/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.json
    try:
        atualizar_turma(id_turma, data)
        return jsonify(turma_por_id(id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'message': 'turma não encontrada'}), 404

@turma_blueprint.route('/turma/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return '', 204
    except TurmaNaoEncontrada:
        return jsonify({'message': 'turma não encontrada'}), 404

