from .mapping_type import MappingType

from image_representation.linear_mapping import LinearMapping
from image_representation.zigzag_mapping import ZigZagMapping
from image_representation.serpentine_mapping import SerpentineMapping

from image_representation.image_mapping_strategy import ImageMappingStrategy

class PEFile:

    def read(self, filePath, mappingType):

        # legge il file PE e mantiene i byte solo internamente alla classe
        byteData = self.__readBytes(filePath)

        # se l'altezza non è stata impostata nel file di configurazione,
        # viene calcolata in base alla dimensione del file
        if ImageMappingStrategy.height is None:
            ImageMappingStrategy.setVariableHeight(
                ImageMappingStrategy.width,
                len(byteData)
            )

        # selezione della strategia di mapping
        if mappingType == MappingType.LINEAR:
            strategy = LinearMapping()

        elif mappingType == MappingType.ZIGZAG:
            strategy = ZigZagMapping()

        elif mappingType == MappingType.SERPENTINE:
            strategy = SerpentineMapping()

        # la strategia costruisce direttamente l'immagine finale
        return strategy.createImage(byteData)

    def __readBytes(self, filePath):

        # apertura e lettura del file in modalità binaria
        with open(filePath, "rb") as file:
            return file.read()