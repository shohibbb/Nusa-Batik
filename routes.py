from flask import Flask, render_template
import requests
import json
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()

api_url = 'http://110.239.71.252:3000/Batik'
headers = {'api-key': 'aad2d02e8b3ba7dcc181dc7e85760f1dfe67725f941675db0306d7610778b741'}
response = requests.get(api_url, headers=headers) 
data = response.json().get('data', [])
s_data = sorted(data, key=lambda x: x['id_batik'], reverse=True)

@app.route("/")
def home():
    four_s_data = s_data[:4]
    return render_template('home.html', data=four_s_data)


@app.route('/article/<int:batik>')
def batik(batik):
   
    selected_article = None
    for items in s_data:
        if items['id_batik'] == batik:
            selected_article = items
            break
    if selected_article:
        return render_template('batik.html', article=selected_article)
    else:
        return 'Artikel tidak ditemukan'

@app.route("/article", methods=['GET'])
def article():
    if data is not None:
        return render_template('article.html', data=s_data)
    else:
        return render_template('article.html', message='Data tidak ditemukan')


@app.route("/process", methods=['POST'])
def process():
    
    if data is not None:
        return render_template('home.html')
    else:
        return render_template('home.html', message='Data tidak ditemukan')

if __name__ == '__main__':
    app.run(debug=True)
