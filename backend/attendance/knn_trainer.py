import os
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
from django.conf import settings

def train_knn_model():
    X = []
    y = []
    enc_dir = os.path.join(settings.MEDIA_ROOT, 'encodings')

    for file in os.listdir(enc_dir):
        if file.endswith(".npy"):
            encoding = np.load(os.path.join(enc_dir, file))
            label = file.replace('.npy', '')
            X.append(encoding)
            y.append(label)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    model_path = os.path.join(settings.MEDIA_ROOT, 'knn_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(knn, f)
    print("✅ KNN model trained and saved.")
