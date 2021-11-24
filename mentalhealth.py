import re
import os,sys
import nltk
import time
import heapq
import socket
import pyttsx3
import threading
from tkinter import *
from bot import chat
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import tkinter.scrolledtext as scrolledtext
from tkcalendar import Calendar, DateEntry
import time,random
import pygame,webbrowser,pyperclip,sqlite3
from plyer import notification
from PIL import Image,ImageTk
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

saved_username = ["You"]
window_size="500x500"

class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)


    # File
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
       # file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Clear Chat", command=self.clear_chat)
      #  file.add_separator()
        file.add_command(label="Exit",command=self.chatexit)

    # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)

        other = Menu(menu, tearoff=0)
        menu.add_cascade(label="Games", menu=other)
        other.add_command(label="a day of slacking", command=self.g1)
        other.add_command(label="cherie disco blair", command=self.g2)
        other.add_command(label="foot ninja", command=self.g3)
        other.add_command(label="red beard", command=self.g4)
        other.add_command(label="save the sheriff", command=self.g5)
        other.add_command(label="tennis ace", command=self.g6)     

        other = Menu(menu, tearoff=0)
        menu.add_cascade(label="Other Apps", menu=other)
        other.add_command(label="Calender", command=self.cale)

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default",command=self.font_change_default)
        font.add_command(label="Times",command=self.font_change_times)
        font.add_command(label="System",command=self.font_change_system)
        font.add_command(label="Helvetica",command=self.font_change_helvetica)
        font.add_command(label="Fixedsys",command=self.font_change_fixedsys)
      
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        #help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="About HOMIE", command=self.msg)

        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        # self.users_message = self.entry_field.get()

        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        
        # send button
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message_insert(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=8)
        self.master.bind("<Return>", self.send_message_insert)
        self.n = Button(self.master, text="  Exit  ",bd=3,relief="solid")
        self.n.pack()
        self.n = Button(self.master, text="Play Relaxing Music",bd=3,relief="solid",command=self.play)
        self.n.place(x=8,y=462)
        self.n = Button(self.master, text="Pause Music",bd=3,relief="solid",command=self.pause)
        self.n.place(x=125,y=462)
        self.n = Button(self.master, text="Search For Doctors",bd=3,relief="solid",command=self.search)
        self.n.place(x=203,y=462)
        self.n = Button(self.master, text="Call For Help",bd=3,relief="solid",command=self.call)
        self.n.place(x=314,y=462)
        self.n = Button(self.master, text="  Helps  ",bd=3,relief="solid",command=self.images)
        self.n.place(x=392,y=462)
        self.color_theme_grey()
        self.send_message_insert_n()
        self.intr()

    def database(self):
        global conn,cursor
        conn=sqlite3.connect("dataset/doctors.db")
        cursor = conn.cursor()
        q = "Create table if not exists doctor (id integer primary key AUTOINCREMENT,name TEXT,email varchar(150) unique,phone_no TEXT,location TEXT,nearby TEXT,Timing TEXT,practo TEXT)"
        cursor.execute(q)

    def search(self):

        searchwin=Tk()
        searchwin.title("Search For Doctors")
        searchwin.geometry("780x500")  
        searchwin.resizable(0,0)
        search=StringVar(searchwin)

        searchwin.config(bg="gray23")

        def searchdata():
            treev.delete(*treev.get_children())
            self.database()
            query ="select id,name,phone_no,location,Timing from doctor"
            cursor.execute(query)
            data = cursor.fetchall()
            for i in range(len(data)):
                if data[i][3]==search.get():
                    treev.insert("",i,text=str(i),values=data[i])


        def searchdataall():
            treev.delete(*treev.get_children())
            self.database()
            query ="select id,name,phone_no,location,Timing from doctor"
            cursor.execute(query)
            data = cursor.fetchall()
            for i in range(len(data)):
                treev.insert("",i,text=str(i),values=data[i])

        def bookap():
            curItem = treev.focus()
            idv = list(treev.item(curItem).values())[2][0]
            idv = int(idv)
            self.database()
            query =f"select practo from doctor where id = {idv}"
            cursor.execute(query)
            data = cursor.fetchone()
            webbrowser.open(data[0])
        h1 = Label(searchwin, text="Search For Doctors",font=("",24,"bold"),bg="gray23",fg="white")
        h1.place(x=230,y=15) 
        h2 = Label(searchwin, text="Location:",font=("",20,"bold"),bg="gray23",fg="white")
        h2.place(x=30,y=100)

        e2 = Entry(searchwin,textvariable=search,font=("",23),width=22,bg="gray10",fg="white")
        e2.place(x=180,y=100)
        b1 = Button(searchwin, text="Search",font=("",15),bd=2,relief="solid",width=15,bg="gray23",fg="white",command=searchdata)
        b1.place(x=559,y=100)

        b2 = Button(searchwin, text="Book An Appointment",font=("",19),bd=2,relief="solid",width=47,bg="#D3D3D3",fg="black",command=bookap)
        b2.place(x=28,y=420)

        treev = ttk.Treeview(searchwin, selectmode ='browse')
          
        # Calling pack method w.r.to treeview
        treev.place(x=30,y=170)

        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(searchwin, 
                                   orient ="vertical", 
                                   command = treev.yview)
          
        # Calling pack method w.r.to verical 
        # scrollbar
        verscrlbar.place(x=30+682+4, y=173, height=200+22)
          
        # Configuring treeview
        treev.configure(xscrollcommand = verscrlbar.set)
          
        # Defining number of columns
        treev["columns"] = ("1", "2", "3","4","5")
          
        # Defining heading
        treev['show'] = 'headings'
          
        # Assigning the width and anchor to  the
        # respective columns
        treev.column("1", width = 80 , anchor ='c')
        treev.column("2", width = 250, anchor ='nw')
        treev.column("3", width = 152, anchor ='nw')
        treev.column("4", width = 100, anchor ='nw')
        treev.column("5", width = 100, anchor ='nw')

        # Assigning the heading names to the 
        # respective columns
        treev.heading("1", text ="S.no.")
        treev.heading("2", text ="Name")
        treev.heading("3", text ="Phone No.")
        treev.heading("4", text ="Location")
        treev.heading("5", text ="Timing")
        searchdataall()
        searchwin.mainloop()

    def cale(self):
        self.top = Tk()
        ttk.Label(self.top, text='Choose date').pack(padx=10, pady=10)
        self.cal = DateEntry(self.top, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.cal.pack(padx=10, pady=10)
        self.top.mainloop()

    def call(self):
        webbrowser.register('chrome',
            None,
            webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open_new("tel:+91982046726") 
        pyperclip.copy("tel:+91982046726")

    def play(self):

        filepath=r"./music/m.mp3"

        #4、# initialization

        pygame.mixer.init()

        # Load music
        track = pygame.mixer.music.load(filepath)

        # play music
        pygame.mixer.music.play()

    def pause(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def images(self):
        """please make sue to install pillow library before running this code  ....
         this project is made by yogesh singh , admin of insatgram page dynamic_codeing ...."""

        class ImageView(object):
            """please make sue to install pillow library before running this code  ....
         this project is made by yogesh singh , admin of insatgram page dynamic_codeing ...."""
            def __init__(self,root):
                self.root = root
                self.root.title("Image-Viewer")
                self.root.geometry('502x627')
                self.root.resizable(0,0)

                # important things ....
                self.i = 0

                # image list 
                self.Image_list = []
                # current path you can use here your default path ok bro .... 
                self.path =r"./images/"
                # possible extensions of images
                self.extension = ['JPG','BMP','PNG']

                # create canvas ...
                self.canvas = Canvas(self.root,bd=5,relief=RIDGE)
                self.canvas.place(x=0,y=0,height=627,width=502)

                # create buttons 

                self.previous_button = Button(self.root,text="⬅",width=3,font=('arial narrow',14,'bold'),command=self.previous_image,bg='white')
                self.previous_button.place(x=5,y=305)

                self.next_button = Button(self.root,text="➡",width=3,font=('arial narrow',14,'bold'),command=self.next_image,bg='white')
                self.next_button.place(x=460,y=305)


                self.open_file()
                self.add_image()

            # open function .....

            def open_file(self):
                self.path = 'D:/Python Project/developed/hackathon/Mental Bot/images' # change the path as per convince
                
                self.Image_list = []
                self.add_image()


            def add_image(self):
                for image in os.listdir(self.path):
                    ext = image.split('.')[::-1][0].upper()
                    if ext in self.extension:
                        self.Image_list.append(image)

                self.resize(self.Image_list[0])

                # resize function 
            def resize(self,image):
                os.chdir(self.path)
                image_p = self.path + '\\'+str(image)
                img = Image.open(image)
                #img.show()
                
                storeobj = ImageTk.PhotoImage(img)
                self.canvas.delete(self.canvas.find_withtag("bacl"))
                self.canvas.image = storeobj  # <--- keep reference of your image
                self.canvas.create_image(0,0,image=storeobj, anchor=NW)

                #print(self.canvas.find_withtag("bacl"))
                self.root.title("Mental Health")


            def next_image(self):
                self.i+=1
                try:
                    self.image = self.Image_list[self.i]
                    self.resize(self.image)
                except:
                    pass

            def previous_image(self):
                self.i -=1
                try:
                    self.image = self.Image_list[self.i]
                    self.resize(self.image)
                except:
                    self.i = 1


        if __name__ == '__main__':
            root = Toplevel()
            img = ImageView(root)
            root.mainloop()
    
    def notification():
        title = "H.O.M.I.E | Quotes"
        txt='''•   “Happiness can be found even in the darkest of times, if one only remembers to turn on the light.”
•   “Promise me you’ll always remember — you’re braver than you believe, and stronger than you seem, and smarter than you think.”
•   “There’s only us. There’s only this. Forget regret, or life is yours to miss. No other road. No other way, no day but today.” 
•   “Your illness is not your identity. Your chemistry is not your character.”
•   “Even if we don’t have the power to choose where we come from, we can still choose where we go from there.”
•   “I am not afraid of storms for I am learning how to sail my ship.”
•   “You are valuable just because you exist. Not because of what you do or what you have done, but simply because you are.” 
•    “Your days are like pages, the chapters unread; you have to keep turning, your book has no end.”
•    “Be patient and tough; someday this pain will be useful to you.”
•    “To love oneself is the beginning of a lifelong romance.”
•   “I have come to realize making yourself happy is most important. Never be ashamed of how you feel. You have the right feel any emotion you want, and do what makes you happy.”
•    “If there is no struggle, there is no progress.” 
•   “I believed in my capacity to stand back up and run into the waves again and again, no matter the risk.”
•   “My dark days made me stronger. Or maybe I already was strong, and they made me prove it.”
•   “You don’t have to be positive all the time. It’s perfectly okay to feel sad, angry, annoyed, frustrated, scared and anxious. Having feelings doesn’t make you a negative person. It makes you human.”
•   “Sometimes the people around you won’t understand your journey. They don’t need to, it’s not for them.”
•   “Tough times never last, but tough people do!”
•   “I keep moving ahead, as always, knowing deep down inside that I am a good person and that I am worthy of a good life.”
•   “Increasing the strength of our minds is the only way to reduce the difficulty of life.”
•   “It’s okay to feel unstable. It’s okay to disassociate. It’s okay to hide from the world. It’s okay to need help. It’s okay not to be okay.
•   “No matter how hard the past, you can always begin again.”
•   “Hope is a powerful thing. Some say it’s a different breed of magic altogether.”
•   “Be thankful for what you have; you'll end up having more. If you concentrate on what you don't have, you will never, ever have enough”
•   “The surest way to make your dreams come true is to live them.”
•   “Dreams don't work unless you take action. The surest way to make your dreams come true is to live them.”
•   “Before you can successfully make friends with others, first you have to become your own friend.”
•   “No matter how small you start, always dream big.”
•   With everything that has happened to you, you can either feel sorry for yourself or treat what has happened as a gift. Everything is either an opportunity to grow or an obstacle to keep you from growing. You get to choose
•   “Positive anything is better than negative nothing.” 
•   “Live life to the fullest, and focus on the positive.”
•   “The greatest glory in living lies not in never failing, but in rising every time we fail.”
•   “If your heart is broken, make art with the pieces.” 
•    “Your attitude is like a box of crayons that color your world. Constantly color your picture gray, and your picture will always be bleak. Try adding some bright colors to the picture by including humor, and your picture begins to lighten up.”
•   “Every day may not be good… but there’s something good in every day.”
•   “The POSITIVE THINKER sees the INVISIBLE, feels the INTANGIBLE, and achieves the IMPOSSIBLE.”
•   “Sorrow looks back, Worry looks around, Faith looks up.”
•   “Always turn a negative situation into a positive situation.” 
•    “The more we make an effort to keep our thoughts positive, the more pleasurable our journey in life will be.” 
•   “If you have positive energy you will always attract positive outcomes.”
•    “To succeed, you need to find something to hold on to, something to motivate you, something to inspire you.” 
•    “Choosing to be positive and having a grateful attitude is going to determine how you’re going to live your life.” 
•   “Be mindful. Be grateful. Be positive. Be true. Be kind.”
•   “Accept yourself, love yourself, and keep moving forward. If you want to fly, you have to give up what weighs you down.”
•   “Live the Life of Your Dreams: Be brave enough to live the life of your dreams according to your vision and purpose instead of the expectations and opinions of others.”
•   “Don't just exist, live.”
•   “Success is not how high you have climbed, but how you make a positive difference to the world.”
•   “Start each day with a positive thought and a grateful heart.”
•   “Never lose hope. Storms make people stronger and never last forever.”
•   “Be thankful for everything that happens in your life; it’s all an experience.”
•   “Stop comparing yourself to other people, just choose to be happy and live your own life.”
•   “Do not set aside your happiness. Do not wait to be happy in the future. The best time to be happy is always now.”
•   It may be raining but the sun always comes out again.
•   Self-care is how you take your power back.”
•   Happiness can be found even in the darkest of times, if one only remembers to turn on the light.”
•   My dark days made me strong. Or maybe I already was strong, and they made me prove it.”
•   Recovery is not one and done. It is a lifelong journey that takes place one day, one step at a time.” 
•   “Out of suffering have emerged the strongest souls; the most massive characters are seared with scars.”
•   “You don’t have to control your thoughts. You just have to stop letting them control you.” 
•   “There is hope even when your brain tells there isn't.”
•   “Don’t believe everything you think.”
•   “Often its deepest pain which empowers you to grow into your highest self.”'''
        message = random.choice(txt.split('\n'))
        notification.notify(title= title,
                    message= message,
                    app_icon = None,
                    timeout= 10,
                    toast=False)   

    notification()

    def playResponce(self,responce):
        x=pyttsx3.init()
        voices = x.getProperty('voices')
        li = []
        if len(responce) > 100:
            if responce.find('--') == -1:
                b = responce.split('--')
                #print(b)
        x.setProperty('voice',voices[0].id)
        x.setProperty('rate',140)
        x.setProperty('volume',100)
        x.say(responce)
        x.runAndWait()
        #print("Played Successfully......")
        
    def g1(self):
        os.popen('./Games/a day of slacking.exe')
    def g2(self):
        os.popen('./Games/cherie disco blair.exe')
    def g3(self):
        os.popen('./Games/foot ninja.exe')
    def g4(self):
        os.popen('./Games/red beard.exe')
    def g5(self):
        os.popen('./Games/save the sheriff.exe')
    def g6(self):
        os.popen('./Games/tennis ace.exe')


    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        sys.exit()

    def msg(self):
        messagebox.showinfo("HOMIE : AI Health Care Chatbot",'HOMIE is a AI healthcare chatbot\nIt is based on retrival-based NLP using pythons NLTK tool-kit module\nGUI is based on Tkinter\nIt can answer any questions with simplified answers \nIt also have some other apps included like calm sounds, calender, games, call for help, book Appointment, Tips and Tricks, motivational Quotes')
    
    def intr(self):
        pr="Welcome To AI Health Care Chatbot \nIn menubar there are many other tools. \nHOMIE is a AI healthcare chatbot\nIt is based on retrival-based NLP using pythons NLTK tool-kit module\nGUI is based on Tkinter\nIt can answer any questions with simplified answers \nIt also have some other apps included like calm sounds, calender, games, call for help, book Appointment, Tips and Tricks, motivational Quotes \n"
        self.text_box.configure(state=NORMAL)
        self.text_box.insert(END, pr)
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)

    def detect(self):
        try:
            emotions=["Anger","disgust","fear","happy","Neutral", "sad", "surprise"]
            json_file = open('./utils/model.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights("./Speech Emotion Detection/Trained_Models/Speech_Emotion_Recognition_Model.h5")
            demo_audio_path = "./music/recording1.wav"
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
            
            tex = emotions[index]
            if tex == "anger":
                ob="Why are you in "+tex
                pr="HOMIE : " + ob + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.entry_field.delete(0,END)
                time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(ob,))
                t2.start()
                
            elif tex == "fear":
                ob="Why you sound so "+tex
                pr="HOMIE : " + ob + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.entry_field.delete(0,END)
                time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(ob,))
                t2.start()       

            elif tex == "happy":
                ob="I'm glad you sound happy"
                pr="HOMIE : " + ob + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.entry_field.delete(0,END)
                time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(ob,))
                t2.start()
                
            elif tex == "sad":
                ob="why are you sad"
                pr="HOMIE : " + ob + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.entry_field.delete(0,END)
                time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(ob,))
                t2.start()

            elif tex == "surprise":
                ob="What surprised you?"
                pr="HOMIE : " + ob + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.entry_field.delete(0,END)
                time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(ob,))
                t2.start()

            elif tex == "disgust":
                ob="Why so serious?"
                pr="HOMIE : " + ob + "\n"
                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, pr)
                self.text_box.configure(state=DISABLED)
                self.text_box.see(END)
                self.entry_field.delete(0,END)
                time.sleep(0)
                t2 = threading.Thread(target=self.playResponce, args=(ob,))
                t2.start()
                                                         
        except:
            pass

    def voice(self):
        # import required libraries
        import sounddevice as sd
        from scipy.io.wavfile import write
        import wavio as wv
        print("!")
        # Sampling frequency
        freq = 44100

        # Recording duration
        duration = 5

        # Start recorder with the given values
        # of duration and sample frequency
        recording = sd.rec(int(duration * freq),
                        samplerate=freq, channels=2)

        # Record audio for the given number of seconds
        sd.wait()

        # Convert the NumPy array to audio file
        wv.write("./music/recording1.wav", recording, freq, sampwidth=2)
        print("!")
        self.detect()

    def send_message_insert_n(self):
    
        user_input = "h"
       

        if user_input.lower()=="h":

            ob="Hello. Please Speak"
            pr="HOMIE : " + ob + "\n"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            self.text_box.configure(state=DISABLED)
            self.text_box.see(END)
            self.entry_field.delete(0,END)
            time.sleep(0)
            t2 = threading.Thread(target=self.playResponce, args=(ob,))
            t2.start()
            self.voice()

    def send_message_insert(self, message):
        try:
            user_input = self.entry_field.get()
            pr1 = "You : " + user_input + "\n"
        except:
            user_input=message

        if user_input.lower()=="None":
            pass

        else:
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr1)
            self.text_box.configure(state=DISABLED)
            self.text_box.see(END)
            #t1 = threading.Thread(target=self.playResponce, args=(user_input,))
            #t1.start()
            #time.sleep(1)
            ob=chat(user_input)
            pr="HOMIE : " + ob + "\n"
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, pr)
            self.text_box.configure(state=DISABLED)
            self.text_box.see(END)
            self.entry_field.delete(0,END)
            time.sleep(0)
            t2 = threading.Thread(target=self.playResponce, args=(ob,))
            t2.start()


        
    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"


            # Grey
    def color_theme_grey(self):
        self.master.config(bg="gray10")
        self.text_frame.config(bg="gray10")
        self.text_box.config(bg="gray20", fg="#ffffff")
        self.entry_frame.config(bg="gray10")
        self.entry_field.config(bg="gray20", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="gray10")
        self.send_button.config(bg="gray20", fg="#ffffff", activebackground="gray20", activeforeground="#ffffff")
        #self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
  

        self.tl_bg = "gray20"
        self.tl_bg2 = "gray10"
        self.tl_fg = "#ffffff"


try:
    socket.create_connection(('google.com',80))
    root=Tk()
    a = ChatInterface(root)
    root.geometry(window_size)
    root.resizable(0,0)
    root.title("AI Health Care Chatbot")
    root.iconbitmap('i.ico')
    root.mainloop()

except:
    x = messagebox.askquestion("AI Health Care Chatbot", "Internet Error!!! Press No to Exit or Press Yes to play dinorun game.")

    if x=='yes':
        os.popen('./Games/dino.exe')
    else:
        exit()
