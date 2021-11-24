from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import ctypes,os
import tkinter.messagebox as tkMessageBox
from tkinter import filedialog
import wave
import keras
import pyaudio,threading
import pandas as pd
import numpy as np
import IPython.display as ipd
# loading json and creating model
from keras.models import model_from_json
from utils.feature_extraction import get_audio_features

def detect(filename):
    try:
        emotions=["Anger","disgust","fear","happy","Neutral", "sad", "surprise"]
        json_file = open('./utils/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("./Speech Emotion Detection/Trained_Models/Speech_Emotion_Recognition_Model.h5")
        demo_audio_path = filename
        ipd.Audio(demo_audio_path)
        demo_mfcc, demo_pitch, demo_mag, demo_chrom = get_audio_features(demo_audio_path,20000)
        mfcc = pd.Series(demo_mfcc)
        pit = pd.Series(demo_pitch)
        mag = pd.Series(demo_mag)
        C = pd.Series(demo_chrom)
        demo_audio_features = pd.concat([mfcc,pit,mag,C],ignore_index=True)
        demo_audio_features= np.expand_dims(demo_audio_features, axis=0)
        demo_audio_features= np.expand_dims(demo_audio_features, axis=2)
        #demo_audio_features.shape
        livepreds = loaded_model.predict(demo_audio_features, 
                                 batch_size=32, 
                                 verbose=1)
        #emotions=["anger","disgust","fear","happy","neutral", "sad", "surprise"]
        index = livepreds.argmax(axis=1).item()
        
        tex = 'Detected Emotion : '+emotions[index]
        print(tex)

    except:
        tex = 'Unable To Detect The Emotion'
        print(tex)

detect("D:/Python Project/developed/hackathon/Mental Bot/Speech Emotion Detection/demo_audio/am-i-totally-screwed-or.wav")
