import pandas as pd
import torch
import torch.nn as nn
from torchvision.io import read_image
from torch.utils.data import Dataset

class ImageDataset(Dataset):

    def __init__(self, imageMapping, needResize, resizeWidth, resizeHeight):

        # lettura del file CSV con imagePath e label
        data = pd.read_csv(imageMapping)

        # salvataggio dei path delle immagini in un array
        self.__images = data["imagePath"].values

        # conversione label in tensori PyTorch
        self.__labels = torch.tensor(data["label"].values, dtype=torch.long)

        # flag per indicare se serve resize
        self.__needResize = needResize

        # dimensioni resize
        self.__resizeWidth = resizeWidth
        self.__resizeHeight = resizeHeight

        # inizializzazione modulo Upsample per il resize delle immagini
        if self.__needResize:

            self.__upsample = nn.Upsample(size=(self.__resizeHeight, self.__resizeWidth), mode="bilinear", align_corners=True)

    def __len__(self):

        return len(self.__labels)

    def __getitem__(self, index):

        # recupero path immagine
        imagePath = self.__images[index]

        # recupero label corrispondente
        label = self.__labels[index]

        # lettura diretta dell'immagine come tensore PyTorch
        image = read_image(imagePath).float()

        # resize dell'immagine se necessario
        if self.__needResize:

            image = image.unsqueeze(0)
            image = self.__upsample(image)
            image = image.squeeze(0)

        return image, label