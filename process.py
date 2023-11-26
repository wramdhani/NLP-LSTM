import json
import random
import nltk
import string
import numpy as np
import pickle
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from keras.utils import pad_sequences

global responses, lemmatizer, tokenizer, le, model, input_shape
input_shape = 14
confidence_threshold = 0.7  # Set your confidence threshold here

# import dataset answer
def load_response():
    global responses
    responses = {}
    with open('bot/data/Intent_KM.json') as content:
        data = json.load(content)
    for intent in data['intents']:
        responses[intent['tag']]=intent['responses']

# import model dan download nltk file
def preparation():
    global lemmatizer, tokenizer, le, model
    load_response()

    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    tokenizer = pickle.load(open('bot/model/tokenizer.pkl', 'rb'))
    le = pickle.load(open('bot/model/labelencoder.pkl', 'rb'))
    lemmatizer = WordNetLemmatizer()
    
    model = load_model('bot/model/chat_model.h5')
    

# hapus tanda baca
def remove_punctuation(text):
    texts_p = []
    text = [letters.lower() for letters in text if letters not in string.punctuation or letters == '?']
    text = ''.join(text)
    texts_p.append(text)
    return texts_p

# mengubah text menjadi vector
def vectorization(texts_p):
    vector = tokenizer.texts_to_sequences(texts_p)
    vector = np.array(vector).reshape(-1)
    vector = pad_sequences([vector], input_shape)
    return vector

# klasifikasi pertanyaan user
def predict(vector):
    output = model.predict(vector)
    confidence = np.max(output) # Get the confidence score
    print("Model Confidence: ", confidence) # debugging
    if confidence < confidence_threshold:
        return 'unknown'
    output = output.argmax()
    response_tag = le.inverse_transform([output])[0]
    return response_tag

# menghasilkan jawaban berdasarkan pertanyaan user
def generate_response(text):
    texts_p = remove_punctuation(text)
    vector = vectorization(texts_p)
    response_tag = predict(vector)
    if response_tag == 'unknown':
        return "Maaf, saya tidak mengerti hal itu. Bisakah Anda memberikan informasi lebih lanjut?"
    answer = random.choice(responses[response_tag])
    return answer
