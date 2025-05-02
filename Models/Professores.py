from config import db

class Professor(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    nome_Professor = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(10), nullable=False)
    Disciplina = db.Column(db.String(50), nullable=False)

    def _init_(self, id, nome_do_Professor, turma, Disciplina):
        self.id = id
        self.nome_do_Professor = nome_do_Professor
        self.turma = turma
        self.Disciplina = Disciplina

    def to_dict(self):
        return {
            "id": self.id,
            "nome_do_Professor": self.nome_do_Professor,
            "turma": self.turma,
            "Disciplina": self.Disciplina
        }


class ProfessorNaoEncontrado(Exception):
    pass


def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    return professor.to_dict()


def listar_professores():
    professores = Professor.query.all()
    return [prof.to_dict() for prof in professores]


def adicionar_professor(professor_dado):
    professor = Professor.query.get(professor_dado['id'])
    if professor is None:
        novo_prof = Professor(
            id=professor_dado['id'],
            nome_do_Professor=professor_dado['nome_do_Professor'],
            turma=professor['turma'],
            Disciplina=professor_dado['Disciplina']
        )
        db.session.add(novo_prof)
        db.session.commit()
    else: 
        return {"message": "Não é possivel adicionar o mesmo Professor já existente."}


def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    professor.nome_do_Professor = novos_dados['nome_do_Professor']
    professor.turma = novos_dados['turma']
    professor.Disciplina = novos_dados['Disciplina']
    db.session.commit()


def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()

