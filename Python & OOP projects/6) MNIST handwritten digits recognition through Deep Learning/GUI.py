from keras.models import load_model
from tkinter import *
import tkinter as Recognizer
import win32gui
from PIL import ImageGrab, Image
import numpy as np

model = load_model('mnist.h5')

def predict_digit(img):
    img = img.resize((28, 28)) # Resizes image to 28x28 pixles
    img = img.convert('L') # Convert rgb to grayscale
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1) # Reshaping to support our model input and normalizing
    img = img / 255.0
    res = model.predict([img])[0] # Predicting the class
    return np.argmax(res), max(res)

class App(Recognizer.Tk):
    def __init__(self):
        Recognizer.Tk.__init__(self)

        self.x = self.y = 0

        # Creating elements
        self.canvas = Recognizer.Canvas(self, width=300, height=300, bg="Gray", cursor="cross")
        self.label = Recognizer.Label(self, text="Write \na \nNumber", font=("Helvetica", 48))
        self.classify_btn = Recognizer.Button(self, text="Analyze", command=self.classify_handwriting)
        self.button_clear = Recognizer.Button(self, text="Reset", command=self.clear_all)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        self.result_label = Recognizer.Label(self, text="", font=("Helvetica", 36))
        self.result_label.grid(row=0, column=2, pady=2, padx=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        self.result_label.configure(text="")

    def classify_handwriting(self):
        HWMD = self.canvas.winfo_id() # Get the handle of the canvas
        rect = win32gui.GetWindowRect(HWMD) # Get the coordinate of the canvas
        a, b, c, d = rect
        rect = (a+4, b+4, c-4, d-4)
        im = ImageGrab.grab(rect)
        digit, acc = predict_digit(im)
        self.result_label.configure(text=f"Prediction: {digit}, Confidence: {int(acc * 100)}%")
        self.canvas.create_text(330, 150, fill="black", font="Helvetica 36 bold", text=f"{digit}, {int(acc * 100)}%")
        self.label.grid_forget()

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='Gold')

app = App()
mainloop()
