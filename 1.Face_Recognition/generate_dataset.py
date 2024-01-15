import os
import pandas as pd
from tqdm import tqdm
from deepface import DeepFace

def generate_dataset(path='/content/drive/MyDrive/PersianFace'):
    data_frame = pd.DataFrame()
    Celebs = []

    for folder in tqdm(os.listdir(path)):
        for img in os.listdir(f'{path}/{folder}'):
            try:
                embedding_objs = DeepFace.represent(img_path = f'{path}/{folder}/{img}', model_name='ArcFace', enforce_detection=False)
            except:
                pass
            df = pd.DataFrame([embedding_objs[0]['embedding']])
            df['Celeb'] = folder
            Celebs.append(folder) if folder not in Celebs else Celebs
            df['Celeb_Label'] = Celebs.index(folder)
            data_frame = data_frame.append(df, ignore_index = True)

    data_frame.to_csv('dataset/dataset.csv')
    data_frame.head()