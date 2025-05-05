from flask_restx import Namespace, Resource, fields
from Models.Professores import listar_professores, adicionar_professor, professor_por_id, atualizar_professor, excluir_professor

professores_ns = Namespace("professores", description="Operações relacionadas aos professores")

professor_input_model = professores_ns.model("ProfessorInput", {
    "nome_do_Professor": fields.String(required=True, description="Nome do professor"),
    "turma": fields.String(required=True, description="Turma do professor"),
    "Disciplina": fields.String(required=True, description="Disciplina ministrada"),
})

professor_output_model = professores_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome_do_Professor": fields.String(description="Nome do professor"),
    "turma": fields.String(description="Turma do professor"),
    "Disciplina": fields.String(description="Disciplina ministrada"),
})

@professores_ns.route("/")
class ProfessorResource(Resource):
    @professores_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista todos os professores"""
        return listar_professores()

    @professores_ns.expect(professor_input_model)
    def post(self):
        """Cria um novo professor"""
        data = professores_ns.payload
        response = adicionar_professor(data)
        return {"message": "Professor criado com sucesso"}, 201

@professores_ns.route("/<int:professor>")
class ProfessorIdResource(Resource):
    @professores_ns.marshal_with(professor_output_model)
    def get(self, professor):
        """Obtém um professor pelo ID"""
        return professor_por_id(professor)

    @professores_ns.expect(professor_input_model)
    def put(self, professor):
        """Atualiza um professor pelo ID"""
        data = professores_ns.payload
        atualizar_professor(professor, data)
        return {"message": "Professor atualizado com sucesso"}, 200

    def delete(self, professor):
        """Exclui um professor pelo ID"""
        excluir_professor(professor)
        return {"message": "Professor excluído com sucesso"}, 200
