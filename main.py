"""docstring"""
import json
import sqlalchemy
from sqlalchemy import String, Integer
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import Flask, render_template, redirect,request

engine = sqlalchemy.create_engine('sqlite:///infinity.db',echo=True,connect_args={'check_same_thread': False})
base = declarative_base()
class Contato(base):
    """criando a tabela"""
    __tablename__ = "contatos"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100))
    celular = Column(String(100))
    tags = Column(String(100))
    links = Column(String(100))
base.metadata.create_all(engine)

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
link_tags = {
    "Trabalho":'https://cdn-icons-png.flaticon.com/512/1395/1395461.png',
    "Familia":'https://cdn-icons-png.flaticon.com/512/2452/2452717.png',
    "Compras":'https://cdn-icons-png.flaticon.com/512/3144/3144456.png'
}

def criar_contato_sql(contato: Contato):#criar contato
    """funcao para criar contato"""
    print('contato criado')
    Session = sessionmaker(bind=engine)
    session = Session()
    #criando a sessao 
    session.add(contato)
    session.commit()
    return 'sucess'

def deletar_contato_sql(identification):#deletar contato
    """funcao para deletar contato"""
    Session = sessionmaker(bind=engine)
    session = Session()
    contato_del = session.query(Contato).filter_by(id=identification).first()
    session.delete(contato_del)
    session.commit()
    return 'sucess'

def editar_contato_sql(identification,contato):#deletar contato
    """funcao para deletar contato"""
    Session = sessionmaker(bind=engine)
    session = Session()
    contato_edit = session.query(Contato).filter_by(id=identification).first()
    contato_edit.nome = contato.nome if contato_edit.nome != contato.nome else contato_edit.nome
    contato_edit.email = contato.email if contato_edit.email != contato.email else contato_edit.email
    contato_edit.celular = contato.celular if contato_edit.celular != contato.celular else contato_edit.celular
    contato_edit.tags = contato.tags if contato_edit.tags != contato.tags else contato_edit.tags
    session.commit()
    return 'sucess'

def buscar_contato_sql():#buscar contato
    """Funcao para buscar todos os contatos"""
    Session = sessionmaker(bind=engine)
    session = Session()
    contatos = session.query(Contato).all()
    return contatos

@app.route('/')
def index():
    """Rota inicial"""
    contatos_ = buscar_contato_sql()
    contatos_aux = []
    if len(contatos_) >0:
        for i ,contato_i in enumerate(contatos_):
            contato_ = contato_i.__dict__
            if len(contato_['tags'])>0:
                contato_['tags'] = contato_['tags'].split(',')
                contato_['links_img_tag'] = [link_tags[chave.title()] for chave in contato_['tags']]
            else:
                contato_['links_img_tag'] = []
            contatos_aux.append(contato_)
    return render_template('index.html',contatos=contatos_aux,link_tags=link_tags)

@app.route('/salvar_contato',methods=['POST',])
def salvar_contato():
    """rota para salvar contato"""
    tags = request.form['tags_val']
    tags = json.loads(tags)
    tags = ','.join([i['tag'] for i in tags])
    cont = Contato(nome=request.form['nome'],
                  email=request.form['email'],
                  celular=request.form['celular'],
                  tags=tags,
                  links='')
    criar_contato_sql(cont)
    return redirect('/')

@app.route('/deletar_contato',methods=['POST',])
def deletar_contato():
    """rota para deletar contato"""
    r = deletar_contato_sql(request.form['id'])
    return redirect('/')

@app.route('/editar_contato',methods=['POST',])
def editar_contato():
    """Rota para deletar contato"""
    tags = request.form['tags_val']
    tags = json.loads(tags)
    tags = ','.join([i['tag'] for i in tags])
    contato = Contato(
        id =request.form['id'],
        nome =request.form['nome'],
        email=request.form['email'],
        celular=request.form['celular'],
        tags=tags,
        links=''
    )
    r = editar_contato_sql(request.form['id'],contato)
    return redirect('/')

@app.route('/buscar_contato',methods=['POST',])
def buscar_contato():
    """Rota para buscar contato"""
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
