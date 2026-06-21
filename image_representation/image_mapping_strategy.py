from abc import ABC, abstractmethod

class ImageMappingStrategy(ABC):

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

        pixels = byteCount // cls.numberOfChannels

        cls.height = (pixels + width - 1) // width

    @abstractmethod
    def createImage(self, data):
        pass