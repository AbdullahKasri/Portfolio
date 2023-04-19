import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image



def get_encoded_faces():
    encoded = {}

    for dirpath, dnames, frames in os.walk("./faces"):
        for f in frames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded

def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]
    return encoding

def classify_face(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    face_locations = face_recognition.face_locations(img)
    unkown_face_encodings = face_recognition.face_encodings(img, face_locations)
    face_names = []

    for face_encoding in unkown_face_encodings:
        matches = face_recognition.compare_faces(faces_encoded, face_encoding) # See if the face is a match for the known face
        name = "Unkown"

        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2) # Draws a box around the face
            cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)
    while True:
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names

UI = tk.Tk()
UI.geometry('450x500')
UI.title('Image recognition system ')
UI.config(background = 'Orange')
label = Label(UI, background = 'Black', font = ('arial', 15, 'bold'))
sign_image = Label(UI)

def show_identify_botton(file_path):
    identify = Button(UI, text = "Identify", command = lambda: classify_face(file_path), padx = 10, pady = 5)
    identify.configure(background = 'White', foreground = 'pink', font = ('arial', 10, 'bold'))
    identify.place(relx = 0.79, rely = 0.46)

def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((UI.winfo_width() / 2.25), (UI.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image = im)
        sign_image.image = im
        label.configure(text = '')
        show_identify_botton(file_path)
    except:
        pass
upload = Button(UI, text = "Upload an image", command = upload_image, padx = 10, pady = 5)
upload.configure(background = 'Red', foreground = 'White', font = ('arial', 10, 'bold'))

UI.mainloop()