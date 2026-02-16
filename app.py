import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)

# importando os dados e lendo eles como csv
def to_csv(file):
    labels = ['wavenumber', 'intensity']
    return pd.read_csv(file, names=labels, sep=None, engine='python')

# funcao pra criar um grafico dos dados
def plot_grafico(x, y, title, xlabel, ylabel):
    plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.plot(x, y)
    
    # salvar grafico em buffer pra enviar como resposta
    img = BytesIO()
    plt.savefig(img, format = 'png')
    img.seek(0)
    return img

@app.route('/upload', methods = ['POST'])
def upload_files():
    # Recebe arquivos do front
    parafina_file = request.files['parafina']
    tecido_file = request.files['tecido']
        
    # monta dataframes
    df_parafina = to_csv(parafina_file)
    df_tecido = to_csv(tecido_file)
        
    # subtrai valores
    m = []
    mx = []
        
    for i in range(len(df_parafina)):
        sub = pd.merge(df_parafina, df_tecido, on='wavenumber', suffixes=('_parafina', '_tecido'))

        sub['intensity'] = sub['intensity_parafina'] - sub['intensity_tecido']

        
        # Coleta o titulo do novo grafico
        title = request.form['title']
        
        # Gera grafico
        img = plot_grafico(
            sub['wavenumber'],
            sub['intensity'],
            title,
            'Wavenumber',
            'Intensity'
        )
        
        # retorna grafico como imagem png
        return send_file(img, mimetype = 'image/png')

if __name__ == '__main__':
    app.run(debug = True)