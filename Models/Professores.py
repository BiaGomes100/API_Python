dados = {
   "professores" : [
    {
        "id": 1,
        "nome_do_Professor": "Maria Souza",
        "turma": "3A",
        "Disciplina": "Ingles"
    },
    {
        "id": 2,
        "nome_do_Professor": "Carlos Mendes",
        "turma": "2B",
        "Disciplina": "Fisica"
    }
   ]
}

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(id_professor):
    lista_professores = dados['professores']
    for dicionario in lista_professores:
        if dicionario['id'] == id_professor:
            return dicionario
    raise ProfessorNaoEncontrado

def listar_professores():
    return dados['professores']

def adicionar_professor(professor):
    dados['professores'].append(professor)

def atualizar_professor(id_professor, novos_dados):
    professor = professor_por_id(id_professor)
    professor.update(novos_dados)

def excluir_professor(id_professor):
    professor = professor_por_id(id_professor)
    dados['professores'].remove(professor)

def apaga_tudo():
    dados['professores'] = []