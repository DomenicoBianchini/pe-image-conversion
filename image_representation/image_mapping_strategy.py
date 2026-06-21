from abc import ABC, abstractmethod

class ImageMappingStrategy(ABC):

    # dimensioni dell'immagine e numero di canali, condivise da tutte le strategie
    width = None
    height = None
    numberOfChannels = None

    @classmethod
    def setImageSize(cls, width, height, numberOfChannels):

        cls.width = width
        cls.height = height
        cls.numberOfChannels = numberOfChannels

    @classmethod
    def setVariableHeight(cls, width, byteCount):

        cls.width = width

        # calcolo del numero di pixel necessari in base ai byte e al numero di canali
        pixels = byteCount // cls.numberOfChannels

        # calcolo dell'altezza necessaria per contenere tutti i pixel, arrotondando per eccesso
        cls.height = (pixels + width - 1) // width

    @abstractmethod
    def createImage(self, data):
        pass