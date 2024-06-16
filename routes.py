from flask import Flask, render_template, request, render_template, session, jsonify, redirect, url_for
from keras._tf_keras.keras.models import load_model
from keras._tf_keras.keras.preprocessing import image
from keras._tf_keras.keras.optimizers import Adam
import requests
import json
import numpy as np
import os
from PIL import Image
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()

api_url = 'http://110.239.71.252:3000/Batik'
headers = {'api-key': 'aad2d02e8b3ba7dcc181dc7e85760f1dfe67725f941675db0306d7610778b741'}
response = requests.get(api_url, headers=headers) 
data = response.json().get('data', [])
s_data = sorted(data, key=lambda x: x['id_batik'], reverse=True)

app.secret_key = os.urandom(24)  # Secret key for session management

# Load and compile the model
model = load_model('batik_classifier.h5')
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Define the list of labels
labels = ['Aceh Pintu Aceh', 'Bali Barong', 'Bali Merak', 'DKI Ondel Onde', 'Jawa Barat Megamendung', 'Jawa Timur Pring', 'Kalimantan Dayak', 'Lampung Gajah', 'Madura Mataketeran', 'Maluku Pala', 'NTB Lumbung', 'Papua Asmat', 'Papua Cendrawasih', 'Papua Tifa', 'Solo Parang', 'Sulawesi Selatan Lontara', 'Sumatera Barat Rumah Minang', 'Sumatera Utara Boraspati', 'Yogyakarta Kawung', 'Yogyakarta Parang']

@app.route("/")
def home():
    four_s_data = s_data[:4]
    return render_template('home.html', data=four_s_data)


@app.route('/article/<string:batik>')
def batik(batik):
   
    selected_article = None
    for items in s_data:
        if items['nama_batik'] == batik:
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
    # Get the uploaded file
    file = request.files['upload']
    if file:
        # Save the file to a specific location
        save_dir = os.path.join(app.root_path, 'static/img/imgPredict')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        filepath = os.path.join(save_dir, file.filename)
        file.save(filepath)
        
        # Preprocess the image
        img = Image.open(filepath).convert('RGB')  # Ensure the image is in RGB format
        img = img.resize((150, 150))  # Resize to 150x150 pixels
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize the image
        
        # Make prediction
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction, axis=1)[0]
        predicted_label = labels[predicted_index]  #Convert index to label
        # Get the predicted probabilities for each class
        prediction_probabilities = prediction[0] 
        # Convert the probabilities to percentages
        prediction_percentages = [f"{prob * 100:.2f}%" for prob in prediction_probabilities]
        # Combine labels with their respective probabilities
        predictions_with_percentages = list(zip(labels, prediction_percentages))
        # Sort predictions by probabilities in descending order
        sorted_predictions = sorted(predictions_with_percentages, key=lambda x: float(x[1][:-1]), reverse=True)
        
        session['prediction'] = predicted_label
        session['file_path'] = filepath
        session['predictions_with_percentages'] = sorted_predictions[:3]  # Store top 3 predictions

        return redirect(url_for('result'))
    else:
        return jsonify({'error': 'No file uploaded'}), 400
    
@app.route('/result')
def result():
    prediction = session.get('prediction', None)
    file_path = session.get('file_path', None)
    predictions_with_percentages = session.get('predictions_with_percentages', None)
    return render_template('result.html', prediction=prediction, file_path=file_path, predictions_with_percentages=predictions_with_percentages)

if __name__ == '__main__':
    app.run(debug=True)
