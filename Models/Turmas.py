dados ={
    "turmas": [
     {
        "id": 1,
        "quantidade_alunos": 25,
        "numero_turma": "3A",
        "professor_representante": "Maria Souza"
    },
    {
        "id": 2,
        "quantidade_alunos": 30,
        "numero_turma": "3B",
        "professor_representante": "Carlos Oliveira"
    },
    ]
}

class TurmaNaoEncontrada(Exception):
    pass

def turma_por_id(id_turma):
    lista_turmas = dados['turmas']
    for dicionario in lista_turmas:
        if dicionario['id'] == id_turma:
            return dicionario
    raise TurmaNaoEncontrada

def listar_turmas():
    return dados['turmas']

def adicionar_turma(turma):
    dados['turmas'].append(turma)

def atualizar_turma(id_turma, novos_dados):
    turma = turma_por_id(id_turma)
    turma.update(novos_dados)

def excluir_turma(id_turma):
    turma = turma_por_id(id_turma)
    dados['turmas'].remove(turma)


def apaga_tudo():
    dados['turmas'] = []