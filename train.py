import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import random
import numpy as np
import pickle
import json
import string 
import re
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential

# Init file
words = []
classes = []
documents = []

data_file = open("intents.json",encoding='utf8')
intents = json.load(data_file)

# init stop words
list_stopwords = set(stopwords.words('english'))

# init stem
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# words
for intent in intents["intents"]:
    for pattern in intent["patterns"]:

        # lowercase pattern
        pattern = pattern.lower()

        # remove punctuation
        pattern = pattern.translate(str.maketrans("","",string.punctuation))
        
        #remove whitespace leading & trailing
        pattern = pattern.strip()
        
        #remove multiple whitespace into single whitespace
        pattern = re.sub('\s+',' ',pattern)
        
        # take each word and tokenize it
        tokens = word_tokenize(pattern)
        words.extend(tokens)

        # remove stop words
        words = [w for w in words if not w in list_stopwords]
        
        # stem
        words = [stemmer.stem(w) for w in words]
        
        # adding documents
        documents.append((tokens, intent["tag"]))

        # adding classes to our class list
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# print(len(documents), "documents")
# print(len(classes), "classes", classes)
# print(len(words), "unique lemmatized words", words)

# save as pickle
pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

# init training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    # init bag of words
    bag = []

    # list of tokenized words for the pattern
    pattern_words = doc[0]
    
    # stem each word - create base word, in attempt to represent related words
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    
    # create bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# shuffle features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists. X - patterns, Y - intents
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print("Training data created")

# model training
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
model.summary()

# compile model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# fit and save the model
history = model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size=8, verbose=1)
model.save("homie_chatbot_model.h5", history)
print("model created")
