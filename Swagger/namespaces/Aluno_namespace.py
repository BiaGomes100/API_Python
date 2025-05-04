from flask_restx import Namespace, Resource, fields
from Models.Alunos import listar_alunos, adicionar_aluno, aluno_por_id, atualizar_aluno, excluir_aluno

alunos_ns = Namespace("alunos", description="Operações relacionadas aos alunos")

aluno_input_model = alunos_ns.model("AlunoInput", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "email": fields.String(required=True, description="Email do aluno"),
    "telefone": fields.String(required=True, description="Telefone do aluno"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "data_nascimento": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "idade": fields.Integer(description="Idade do aluno"),
    "email": fields.String(description="Email do aluno"),
    "telefone": fields.String(description="Telefone do aluno"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return listar_alunos()
    
    @alunos_ns.expect(aluno_input_model)
    def post(self):
        """Cria um novo aluno"""
        data = alunos_ns.payload
        response, status_code = adicionar_aluno(data)
        return response, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        return aluno_por_id(id_aluno)

    @alunos_ns.expect(aluno_input_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        data = alunos_ns.payload
        atualizar_aluno(id_aluno, data)
        return {"message": "Aluno atualizado com sucesso"}, 200

    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        excluir_aluno(id_aluno)
        return {"message": "Aluno excluído com sucesso"}, 200
