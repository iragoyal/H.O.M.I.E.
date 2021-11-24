import random
import numpy as np
import pickle
import json

import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

import string 
import re

from tensorflow.keras.models import load_model

# chat initialization
model = load_model("ella_chatbot_model.h5")
intents = json.loads(open("intents.json", encoding="utf8").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# init stop words
list_stopwords = set(stopwords.words('english'))

# stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def chatbot_message(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def preprocess_sentence(sentence):
    # lowercase pattern
    sentence_words = sentence.lower()

    # remove punctuation
    sentence_words = sentence.translate(str.maketrans("","",string.punctuation))
        
    # remove whitespace leading & trailing
    sentence_words = sentence.strip()
        
    # remove multiple whitespace into single whitespace
    sentence_words = re.sub('\s+',' ',sentence)    
    
    # tokenize
    sentence_words = word_tokenize(sentence)
    
    # remove stop words
    words = [w for w in sentence_words if not w in list_stopwords]

    # stem
    sentence_words = [stemmer.stem(w) for w in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):

    # tokenize the pattern
    sentence_words = preprocess_sentence(sentence)

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        print(r)
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            return result

def chat(inp):
    x=chatbot_message(inp)
    out = str(x)
    return out
chat("hello")