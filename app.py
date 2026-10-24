import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# ---------------- CONFIG ----------------
IMG_HEIGHT = 128
IMG_WIDTH = 128
MODEL_PATH = "model/action_recognition_model.h5"

# Update class names EXACTLY as your dataset folders
CLASS_NAMES = ['kick', 'punch', 'selfie']
# ----------------------------------------

# Load trained model
model = load_model(MODEL_PATH)

# Create main window
root = tk.Tk()
root.title("Action Recognition System")
root.geometry("500x550")
root.resizable(False, False)

# Title label
title = Label(root, text="Action Recognition CNN", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Image display label
image_label = Label(root)
image_label.pack(pady=10)

# Prediction label
result_label = Label(root, text="Prediction: ---", font=("Arial", 14))
result_label.pack(pady=10)

# Function to preprocess image
def preprocess_image(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array, img

# Function to load image and predict
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )

    if not file_path:
        return

    img_array, img = preprocess_image(file_path)

    # Prediction
    preds = model.predict(img_array)
    class_index = np.argmax(preds)
    confidence = preds[0][class_index] * 100

    prediction_text = f"Prediction: {CLASS_NAMES[class_index]}\nConfidence: {confidence:.2f}%"
    result_label.config(text=prediction_text)

    # Display image
    img_display = img.resize((300, 300))
    img_tk = ImageTk.PhotoImage(img_display)
    image_label.config(image=img_tk)
    image_label.image = img_tk

# Open image button
btn = Button(root, text="Select Image", command=open_image, font=("Arial", 12))
btn.pack(pady=15)

# Exit button
exit_btn = Button(root, text="Exit", command=root.destroy, font=("Arial", 12))
exit_btn.pack(pady=5)

# Run app
root.mainloop()
