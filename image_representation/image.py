import numpy as np
from PIL import Image as PILImage

class Image:

    def __init__(self, data):
        self.data = data

    def getWidth(self):
        return self.data.shape[1]

    def getHeight(self):
        return self.data.shape[0]

    def getNumberOfChannels(self):
        return self.data.shape[2]

    def resize(self, width, height):

        # creazione dell'immagine PIL in base al numero di canali
        if self.getNumberOfChannels() == 1:
            image = PILImage.fromarray(self.data[:, :, 0], mode="L")
        else:
            image = PILImage.fromarray(self.data, mode="RGB")

        # ridimensionamento dell'immagine tramite interpolazione bilineare
        image = image.resize((width, height), resample=PILImage.Resampling.BILINEAR)
        data = np.array(image)
        if self.getNumberOfChannels() == 1:
            data = data.reshape(height, width, 1)

        return Image(data)

    def save(self, fileName):

        # salvataggio dell'immagine in base al numero di canali
        if self.getNumberOfChannels() == 1:
            image = PILImage.fromarray(self.data[:, :, 0], mode="L")
        else:
            image = PILImage.fromarray(self.data, mode="RGB")

        image.save(fileName)