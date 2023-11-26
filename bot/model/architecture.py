import json
import pickle
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

# Load your intents
with open('bot/data/Intent_KM.json') as content:
    data = json.load(content)

patterns = []
tags = []

for intent in data['intents']:
    for tag in intent['tag']:
        tags.append(tag)
        patterns.append(intent['patterns'])

# Preprocess your patterns
tokenizer = Tokenizer()
tokenizer.fit_on_texts(patterns)
x_train = tokenizer.texts_to_sequences(patterns)
x_train = pad_sequences(x_train, maxlen=20, padding='post')

# Encode your tags
le = LabelEncoder()
y_train = le.fit_transform(tags)
y_train = to_categorical(y_train)

# Train your model
model = Sequential()
# ... add layers to your model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=200, batch_size=5, verbose=1)

# Save your model and encoders
model.save('bot/model/chat_model.h5')
pickle.dump(tokenizer, open('bot/model/tokenizer.pkl', 'wb'))
pickle.dump(le, open('bot/model/labelencoder.pkl', 'wb'))
