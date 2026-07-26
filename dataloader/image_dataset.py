import pandas as pd
import torch
import torch.nn as nn
from torchvision.io import read_image, ImageReadMode
from torchvision.transforms import Normalize
from torch.utils.data import Dataset

class ImageDataset(Dataset):

    def __init__(self, imageLabelsPath, needResize, resizeWidth, resizeHeight):

        # lettura del file CSV con imagePath e label
        data = pd.read_csv(imageLabelsPath)

        # salvataggio dei path delle immagini in una lista
        self.__images = data["imagePath"].tolist()

        # salvataggio delle label in una lista
        self.__labels = data["label"].tolist()

        # flag per indicare se serve resize
        self.__needResize = needResize

        # dimensioni resize
        self.__resizeWidth = resizeWidth
        self.__resizeHeight = resizeHeight

        # inizializzazione modulo Upsample per il resize delle immagini
        if self.__needResize:

            self.__upsample = nn.Upsample(size=(self.__resizeHeight, self.__resizeWidth), mode="bilinear", align_corners=True)

        # normalizzazione per ResNet
        self.__normalize = Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    def __len__(self):

        return len(self.__labels)

    def __getitem__(self, index):

        # recupero path immagine
        imagePath = self.__images[index]

        # recupero label corrispondente
        label = torch.tensor(self.__labels[index], dtype=torch.long)

        # lettura diretta dell'immagine come tensore PyTorch
        image = read_image(imagePath, mode=ImageReadMode.RGB).float()

        # conversione valori da 0-255 a 0-1
        image = image / 255.0

        # resize dell'immagine se necessario
        if self.__needResize:

            image = image.unsqueeze(0)
            image = self.__upsample(image)
            image = image.squeeze(0)

        # normalizzazione per ResNet
        image = self.__normalize(image)

        return image, label