import os
import pandas as pd
from tqdm import tqdm
from deepface import DeepFace

def generate_dataset(path='/content/drive/MyDrive/PersianFace'):
    dataset = []

    for folder in tqdm(os.listdir(path)):
        for img in os.listdir(f'{path}/{folder}'):
            try:
                embedding_objs = DeepFace.represent(img_path = f'{path}/{folder}/{img}', model_name='ArcFace')
            except:
                pass
            dict_img = embedding_objs[0]
            dict_img['label'] = folder
            dataset.append(dict_img) 

    df = pd.DataFrame(dataset)
    df.to_csv('dataset/dataset.csv')


