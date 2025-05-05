import os
from config import app,db
from Controllers.Aluno_Controller import alunos_blueprint
from Controllers.Turma_Controller import turma_blueprint
from Controllers.Professor_Controller import professores_blueprint


app.register_blueprint(alunos_blueprint,url_prefix = "/api")
app.register_blueprint(turma_blueprint,url_prefix = "/api")
app.register_blueprint(professores_blueprint,url_prefix = "/api")

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
  app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG'] )    