from config import db

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_turma = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    turno = db.Column(db.String(20), nullable=False)

    def __init__(self, nome_turma, ano, turno):
        self.nome_turma = nome_turma
        self.ano = ano
        self.turno = turno

    def to_dict(self):
        return {
            'id': self.id,
            'nome_turma': self.nome_turma,
            'ano': self.ano,
            'turno': self.turno
        }


class TurmaNaoEncontrada(Exception):
    pass


def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.to_dict()


def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]


def adicionar_turma(turma_data):
    nova_turma = Turma(
        nome_turma=turma_data['nome_turma'],
        ano=turma_data['ano'],
        turno=turma_data['turno']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return {"message": "professor adicionado com sucesso!", "body": nova_turma.id}, 201


def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if turma is None:
        raise TurmaNaoEncontrada()

    if 'nome_turma' in novos_dados:
        turma.nome_turma = novos_dados['nome_turma']
    if 'ano' in novos_dados:
        turma.ano = novos_dados['ano']
    if 'turno' in novos_dados:
        turma.turno = novos_dados['turno']

    db.session.commit()

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()
