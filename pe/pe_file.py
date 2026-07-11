import os

from .mapping_type import MappingType
from image_representation.linear_mapping import LinearMapping
from image_representation.zigzag_mapping import ZigZagMapping
from image_representation.serpentine_mapping import SerpentineMapping
from image_representation.image_mapping_strategy import ImageMappingStrategy

class PEFile:

    def PEToImage(self, filePath, imagesPath, mappingType):

        # apertura e lettura del file PE in modalità binaria
        with open(filePath, "rb") as file:
            byteData = file.read()

        # selezione della strategia di mapping
        if mappingType == MappingType.LINEAR:
            strategy = LinearMapping()

        elif mappingType == MappingType.ZIGZAG:
            strategy = ZigZagMapping()

        elif mappingType == MappingType.SERPENTINE:
            strategy = SerpentineMapping()

        # creazione dell'immagine a partire dai byte del file PE
        image = strategy.createImage(byteData)

        # salvataggio dell'immagine generata
        fileName = os.path.basename(filePath)
        outputImage = os.path.join(imagesPath, fileName + ".png")
        image.save(outputImage)