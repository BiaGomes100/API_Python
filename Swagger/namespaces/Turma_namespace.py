from flask_restx import Namespace, Resource, fields
from Models.Turmas import listar_turmas, adicionar_turma, turma_por_id, atualizar_turma, excluir_turma

turmas_ns = Namespace("turmas", description="Operações relacionadas às turmas")

turma_input_model = turmas_ns.model("TurmaInput", {
    "nome_turma": fields.String(required=True, description="Nome da turma"),
    "ano": fields.Integer(required=True, description="Ano da turma"),
    "turno": fields.String(required=True, description="Turno da turma"),
})

turma_output_model = turmas_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "nome_turma": fields.String(description="Nome da turma"),
    "ano": fields.Integer(description="Ano da turma"),
    "turno": fields.String(description="Turno da turma"),
})

@turmas_ns.route("/")
class TurmaResource(Resource):
    @turmas_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista todas as turmas"""
        return listar_turmas()

    @turmas_ns.expect(turma_input_model)
    def post(self):
        """Cria uma nova turma"""
        data = turmas_ns.payload
        response = adicionar_turma(data)
        return response or {"message": "Turma criada com sucesso"}, 201

@turmas_ns.route("/<int:turma>")
class TurmaIdResource(Resource):
    @turmas_ns.marshal_with(turma_output_model)
    def get(self, turma):
        """Obtém uma turma pelo ID"""
        return turma_por_id(turma)

    @turmas_ns.expect(turma_input_model)
    def put(self, turma):
        """Atualiza uma turma pelo ID"""
        data = turmas_ns.payload
        atualizar_turma(turma, data)
        return {"message": "Turma atualizada com sucesso"}, 200

    def delete(self, turma):
        """Exclui uma turma pelo ID"""
        excluir_turma(turma)
        return {"message": "Turma excluída com sucesso"}, 200
