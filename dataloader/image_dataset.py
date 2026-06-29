import pandas as pd
import torch
import numpy as np
from torch.utils.data import Dataset
from PIL import Image

class ImageDataset(Dataset):

    def __init__(self, imagesPath, labelsPath):

        # percorso della cartella con le immagini
        self.__imagesPath = imagesPath

        # lettura del CSV
        labels = pd.read_csv(labelsPath)

        # salviamo i nomi delle immagini
        self.__filenames = labels["filename"].values

        # convertiamo le label in tensori PyTorch
        self.__labels = torch.tensor(labels["label"].values, dtype=torch.long)


    def __len__(self):

        return len(self.__labels)


    def __getitem__(self, index):

        # recupero nome immagine
        filename = str(self.__filenames[index])

        # recupero label già convertita
        label = self.__labels[index]

        # costruzione percorso immagine
        imagePath = self.__imagesPath + "/" + filename + ".png"

        # apertura immagine
        image = Image.open(imagePath)

        # conversione immagine in tensore PyTorch
        image = torch.tensor(np.array(image), dtype=torch.float32)

        return image, label