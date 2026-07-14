import numpy as np
from PIL import Image as PILImage

class Image:

    def __init__(self, data):

        self.__data = data

    def getWidth(self):

        return self.__data.shape[1]

    def getHeight(self):

        return self.__data.shape[0]

    def getNumberOfChannels(self):

        return self.__data.shape[2]

    def save(self, fileName):

        # salvataggio dell'immagine in base al numero di canali
        if self.getNumberOfChannels() == 1:
            image = PILImage.fromarray(self.__data[:, :, 0], mode="L")
        else:
            image = PILImage.fromarray(self.__data, mode="RGB")

        image.save(fileName)