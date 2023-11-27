import json
import pickle
import nltk
import pandas as pd
import string
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Embedding, LSTM, Flatten, Dense
from nltk.stem import WordNetLemmatizer

# Downloading NTLK Packages
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Load your intents
with open('bot/data/Intent_KM.json') as content:
    data = json.load(content)

patterns = []
tags = []
words = []
responses = {}
ignore_words = ['?', '!']
documents = []
classes = []
inputs = []

for intent in data['intents']:
    responses[intent['tag']]=intent['responses']
    for lines in intent['patterns']:
        inputs.append(lines)
        tags.append(intent['tag'])
    # digunakan untuk pattern atau teks pertanyaan dalam json
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        # tambahkan ke dalam list kelas dalam data
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Json to Dataframe conversion
df = pd.DataFrame({"patterns":inputs, "tags":tags})

# Removing Punctuations
df['patterns'] = df['patterns'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
df['patterns'] = df['patterns'].apply(lambda wrd: ''.join(wrd))
lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Preprocess your patterns
tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['patterns'])
x_train = tokenizer.texts_to_sequences(df['patterns'])
x_train = pad_sequences(x_train)

# Encode your tags
le = LabelEncoder()
y_train = le.fit_transform(df['tags'])
# y_train = to_categorical(y_train)

# Pembentukan Layer
input_shape = x_train.shape[1]
vocabulary = len(tokenizer.word_index)
output_length = le.classes_.shape[0]

# Save your model and encoders
pickle.dump(words, open('bot/model/words.pkl','wb'))
pickle.dump(classes, open('bot/model/classes.pkl','wb'))
pickle.dump(le, open('bot/model/labelencoder.pkl', 'wb'))
pickle.dump(tokenizer, open('bot/model/tokenizer.pkl', 'wb'))

# Membuat model
i = Input(shape=(input_shape,)) # Input Layer
x = Embedding(vocabulary+1,10)(i) # Embedding Layer
x = LSTM(10, return_sequences=True, recurrent_dropout=0.2)(x) # LSTM Layer
x = Flatten()(x) # Flatten Layer
x = Dense(output_length, activation="softmax")(x) # Dense Layer
model = Model(i, x) # Structured Model with input and output Layers

# ... add layers to your model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train your model
model.fit(x_train, y_train, epochs=450)

model.save('bot/model/chat_model.h5')
