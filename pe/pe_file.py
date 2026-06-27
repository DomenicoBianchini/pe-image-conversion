import os

from .mapping_type import MappingType
from image_representation.linear_mapping import LinearMapping
from image_representation.zigzag_mapping import ZigZagMapping
from image_representation.serpentine_mapping import SerpentineMapping
from image_representation.image_mapping_strategy import ImageMappingStrategy

class PEFile:

    def read(self, filesPath, mappingType):

        # lettura di tutti i file PE presenti nella cartella
        for fileName in os.listdir(filesPath):

            filePath = os.path.join(filesPath, fileName)

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

            # se l'altezza è variabile, ridimensiona l'immagine per la CNN
            if ImageMappingStrategy.getHeight() is None:
                targetSize = ImageMappingStrategy.getWidth()
                image = image.resize(targetSize, targetSize)

            # salvataggio dell'immagine generata con le dimensioni finali nel nome
            outputPath = "images/" + os.path.splitext(fileName)[0] + "_" + str(image.getWidth()) + "x" + str(image.getHeight()) + ".png"
            image.save(outputPath)