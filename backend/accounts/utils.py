import os
import numpy as np
import face_recognition
from django.conf import settings
from attendance.knn_trainer import train_knn_model

def save_face_encoding(user, face_img):
    faces_dir = os.path.join(settings.MEDIA_ROOT, 'faces')
    enc_dir = os.path.join(settings.MEDIA_ROOT, 'encodings')
    os.makedirs(faces_dir, exist_ok=True)
    os.makedirs(enc_dir, exist_ok=True)

    image_path = os.path.join(faces_dir, f"{user.id}_{user.name}.jpg")
    with open(image_path, 'wb+') as f:
        for chunk in face_img.chunks():
            f.write(chunk)

    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        np.save(os.path.join(enc_dir, f"{user.id}.npy"), encodings[0])
        train_knn_model()