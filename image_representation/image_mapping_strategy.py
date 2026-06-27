from abc import ABC, abstractmethod

class ImageMappingStrategy(ABC):

    # dimensioni dell'immagine e numero di canali, condivise da tutte le strategie
    __width = None
    __height = None
    __numberOfChannels = None

    @classmethod
    def setImageSize(cls, width, height, numberOfChannels):

        cls.__width = width
        cls.__height = height
        cls.__numberOfChannels = numberOfChannels

    @classmethod
    def getVariableHeight(cls, byteCount):

        # calcolo dell'altezza necessaria senza modificare la configurazione
        pixels = byteCount // cls.__numberOfChannels
        height = (pixels + cls.__width - 1) // cls.__width

        return height

    @classmethod
    def getWidth(cls):

        return cls.__width

    @classmethod
    def getHeight(cls):

        return cls.__height

    @classmethod
    def getNumberOfChannels(cls):

        return cls.__numberOfChannels

    @abstractmethod
    def createImage(self, data):
        pass