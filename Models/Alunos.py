from datetime import date
from config import db

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_Aluno = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=True)

    def __init__(self, nome_Aluno , data_nascimento , email , telefone):
        self.nome_Aluno = nome_Aluno
        self.data_nascimento = data_nascimento
        self.email = email
        self.telefone = telefone

    def calcular_idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome_Aluno,
            'data_nascimento': self.data_nascimento.isoformat(),
            'idade': self.calcular_idade(),
            'email': self.email,
            'telefone': self.telefone
        }

class AlunoNaoEncontrado(Exception):
    pass


def aluno_por_id(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()


def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]


def adicionar_aluno(aluno_data):
    novo_aluno = Aluno(
        nome_Aluno=aluno_data['nome'],
        data_nascimento=aluno_data['data_nascimento'],
        email=aluno_data['email'],
        telefone=aluno_data.get('telefone')  
    )
    db.session.add(novo_aluno)
    db.session.commit()


def atualizar_aluno(id_aluno, novos_dados):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    aluno.nome_Aluno = novos_dados['nome']
    aluno.data_nascimento = novos_dados['data_nascimento']
    aluno.email = novos_dados['email']
    aluno.telefone = novos_dados.get('telefone')
    db.session.commit()


def excluir_aluno(id_aluno):
    aluno = Aluno.query.get(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()