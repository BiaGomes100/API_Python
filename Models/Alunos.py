from datetime import date, datetime
from config import db

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=True)

    def __init__(self, nome, data_nascimento, email, telefone):
        self.nome = nome
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
            'nome': self.nome,
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


def adicionar_aluno(aluno_dado):
    campos_obrigatorios = ['nome', 'data_nascimento', 'email']
    for campo in campos_obrigatorios:
        if campo not in aluno_dado:
            return {"message": f"Campo obrigatório faltando: {campo}"}, 400

    if Aluno.query.filter_by(email=aluno_dado['email']).first():
        return {"message": "Email já cadastrado."}, 400

    novo_aluno = Aluno(
        nome=aluno_dado['nome'],
        data_nascimento=datetime.strptime(aluno_dado['data_nascimento'], "%Y-%m-%d").date(),
        email=aluno_dado['email'],
        telefone=aluno_dado.get('telefone')
    )

    db.session.add(novo_aluno)
    db.session.commit()
    return {"message": "Aluno adicionado com sucesso!", "body": novo_aluno.id}, 201
    


def atualizar_aluno(id, novos_dados):
    aluno = Aluno.query.get(id)
    if aluno is None:
        raise AlunoNaoEncontrado()

    if 'nome' in novos_dados:
        aluno.nome_Aluno = novos_dados['nome']
    if 'data_nascimento' in novos_dados:
        aluno.data_nascimento = datetime.strptime(novos_dados['data_nascimento'], "%Y-%m-%d").date()
    if 'email' in novos_dados:
        aluno.email = novos_dados['email']
    if 'telefone' in novos_dados:
        aluno.telefone = novos_dados['telefone']

    db.session.commit()


def excluir_aluno(id):
    aluno = Aluno.query.get(id)
    if aluno is None:
        raise AlunoNaoEncontrado()
    db.session.delete(aluno)
    db.session.commit()

def apaga_tudo():
    db.session.query(Aluno).delete()
    db.session.commit()