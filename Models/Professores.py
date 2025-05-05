from config import db

class Professor(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    nome_professor = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(10), nullable=False)
    disciplina = db.Column(db.String(50), nullable=False)

    def _init_(self, nome_professor, turma, disciplina):
        self.nome_professor = nome_professor
        self.turma = turma
        self.disciplinaisciplina = disciplina

    def to_dict(self):
        return {
            'id': self.id,
            "nome_professor": self.nome_professor,
            "turma": self.turma,
            "disciplina": self.disciplina
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
    novo_prof = Professor(
        nome_professor=professor_dado['nome_professor'],
        turma=professor_dado['turma'],
        disciplina=professor_dado['disciplina']
    )
    db.session.add(novo_prof)
    db.session.commit()
    return {"message": "professor adicionado com sucesso!", "body": novo_prof.id}, 201
   
   
def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado

    if 'nome_professor' in novos_dados:
        professor.nome_professor = novos_dados['nome_professor']
    if 'turma' in novos_dados:
        professor.turma = novos_dados['turma']
    if 'disciplina' in novos_dados:
        professor.disciplina = novos_dados['disciplina']

    db.session.commit()


def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()


def apaga_tudo():
    db.session.query(Professor).delete()
    db.session.commit()
