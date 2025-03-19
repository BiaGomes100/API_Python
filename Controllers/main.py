import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.Controllers.')))
from Aluno_Controller import *
from Professor_Controller import *
from Turma_Controller import *

from TestesAluno import *
from TesteProfessor import *
from TesteTurma import *
from flask import Flask, json, make_response,jsonify,request 

app = Flask(__name__)

testeAluno = Teste()
testeAluno.teste_get 
testeAluno.testeAdicionar
testeAluno.testeAdicionarAlunoInvalido
testeAluno.testeDeletar
testeAluno.testeDeletarAlunoNaoEncontrado


TesteProfessores = TesteProfessores()
TesteProfessores.teste_get
TesteProfessores.testeAdicionar
TesteProfessores.testeAtualizar
TesteProfessores.testeDeletar
TesteProfessores.testeDeletarProfessorNaoEncontrado


TesteTurmas = TesteTurmas()
TesteTurmas.teste_get 
TesteTurmas.teste_get_por_ID
TesteTurmas.testeAdicionar
TesteTurmas.testeAtualizar
TesteTurmas.testeDeletar_por_ID



if __name__ == '__main__':
    app.run(debug=True)