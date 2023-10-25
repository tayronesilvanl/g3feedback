from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

# Inicialização da instância Flask
app = Flask(__name__)

# Configuração do SQLAlchemy para conexão com o PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:hNX0AUk2mVew@ep-falling-mode-59025380.us-east-1.postgres.vercel-storage.com:5432/verceldb"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Feedback para representar a tabela no banco de dados
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atendimento = db.Column(db.String(50), nullable=False)
    veiculo = db.Column(db.String(50), nullable=False)
    conducao = db.Column(db.String(50), nullable=False)
    satisfacao = db.Column(db.String(50), nullable=False)
    comentarios = db.Column(db.Text)

# Rota principal para exibir o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o formulário submetido
@app.route('/submit', methods=['POST'])
def submit():
    resposta_atendimento = request.form['resposta_atendimento']
    resposta_veiculo = request.form['resposta_veiculo']
    resposta_conducao = request.form['resposta_conducao']
    resposta_satisfacao = request.form['resposta_satisfacao']
    resposta_comentarios = request.form['resposta_comentarios']

    # Criar uma instância do modelo Feedback e preenchê-lo com os dados do formulário
    feedback = Feedback(
        atendimento=resposta_atendimento,
        veiculo=resposta_veiculo,
        conducao=resposta_conducao,
        satisfacao=resposta_satisfacao,
        comentarios=resposta_comentarios
    )

    # Adicionar e salvar (commit) o feedback no banco de dados
    db.session.add(feedback)
    db.session.commit()

    return redirect(url_for('index'))

# Função para adicionar dados ao arquivo Excel (se você ainda quiser usar)
def adicionar_dados_excel(data):
    if not os.path.exists('resultados.xlsx'):
        df = pd.DataFrame(data)
        df.to_excel('resultados.xlsx', index=False)
    else:
        df_existente = pd.read_excel('resultados.xlsx')
        df_novo = pd.DataFrame(data)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        df_final.to_excel('resultados.xlsx', index=False)

# Ponto de entrada principal
if __name__ == '__main__':
    app.run(debug=True)
