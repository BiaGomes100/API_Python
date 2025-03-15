# serve para o python entender que API_PYTHON é o diretorio raiz do projeto fazendo ele identificar mais facil as pastas
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask, make_response,jsonify,request ##importando o Flask
from Models.Turmas import *

app = Flask(__name__) ##instanciando o Flask para poder ser usado
app.config['JSON_SORT_KEYS']= False #faz com que não ordene o respose de AaZ

@app.route('/Turma/BuscarTurmaPorID', methods=['GET'])
def buscarTurma_id():
       turmaParaBuscar = request.json
       id = verificarID(turmaParaBuscar['id'])
       if id == True:
           return  make_response( 
                  jsonify(
                      mensagem = 'erro:',
                     dados = "id vazio"
            ) 
           )  
       else: 
             for turma in turmas:
                if turma["id"] == turmaParaBuscar["id"]:
                    return make_response(jsonify(
                        mensagem='Turma encontrada:',
                        dados=turma
                    ), 200)  

                return make_response(jsonify(
                    mensagem='Turma não encontrada',
                    dados=None
                ), 404) 


@app.route('/Turma/BuscarTurma', methods=['GET'])  ##decorator serve para dar uma funcionalidade para a função abaixo, essa por exemplo serve para inicializar a função
def buscarTurmas():
    return make_response( 
        jsonify(
            mensagem = 'Lista de turmas',
            dados = turmas
            ) #transforma em json bonitinho
    )

@app.route('/Turma/AdicionarTurma', methods=['POST'])
def adicionar_turma():
    turma = request.json
    requestVazia = validarTurma
    if requestVazia == False:
        return  make_response(jsonify(
                    mensagem='Erro: Todos os campos são obrigatórios.',
                    dados=None
                ), 404) 
    else:
        turmas.append(turma)
        return make_response(
            jsonify(
                mensagem = 'Turma cadastrado com sucesso!',
                dado = turma
                ),200
            )

@app.route('/Turma/AtualizarTurma/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    dados_atualizados = request.json

  
    if not validarTurma(dados_atualizados):
        return make_response(jsonify(
            mensagem="Erro: Todos os campos são obrigatórios.",
            dados=None
        ), 400)
    
    
    for turma in turmas:
        if turma["id"] == id:
            turma.update(dados_atualizados)  # Atualiza os dados da turma
            return make_response(jsonify(
                mensagem="Turma atualizada com sucesso!",
                dados=turma
            ), 200)
    
    # Se não encontrar a turma
    return make_response(jsonify(
        mensagem="Erro: Turma não encontrada.",
        dados=None
    ), 404)

@app.route('/Turma/DeletarTurmaPorID', methods=['DELETE'])
def deletar_turma():
    turmaParaDeletar = request.json
     
    id = verificarID(turmaParaDeletar['id'])
    if id == True:
         return  make_response( 
                  jsonify(
                      mensagem = 'erro:',
                     dados = "id vazio"
            ),404 
           )  
    else:
        for turma in turmas:
            if turma["id"] == turmaParaDeletar["id"]:
                turmas.remove(turma)
                return make_response(
                    jsonify(
                        mensagem= 'Turma excluído com sucesso!',
                        dado = turma
                    ),200
                )
        return make_response(jsonify(
                    mensagem="Erro: id não encontrada.",
                    dados=None
                ), 404)
            


app.run()



def verificarID(id):
    if id == None:
        return True
    else: 
        return False



def validarTurma(turma):
    campos_obrigatorios = ["id", "quantidade_alunos", "numero_turma", "professor_representante"]
    
    # Retorna False se algum campo estiver ausente ou vazio
    for campo in campos_obrigatorios:
        if campo not in turma or turma[campo] in [None, ""]:
            return False
    
    return True  