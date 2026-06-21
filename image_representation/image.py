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

    def save(self, fileName):
        if self.getNumberOfChannels() == 1:
            image = PILImage.fromarray(self.data[:, :, 0], mode="L")
        else:
            image = PILImage.fromarray(self.data, mode="RGB")

        image.save(fileName)