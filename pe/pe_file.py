from .mapping_type import MappingType

from image_representation.linear_mapping import LinearMapping
from image_representation.zigzag_mapping import ZigZagMapping
from image_representation.serpentine_mapping import SerpentineMapping

from image_representation.image_mapping_strategy import ImageMappingStrategy

class PEFile:

    def read(self, filePath, mappingType):

        byteData = self.__readBytes(filePath)

        if ImageMappingStrategy.height is None:
            ImageMappingStrategy.setVariableHeight(
                ImageMappingStrategy.width,
                len(byteData)
            )

        if mappingType == MappingType.LINEAR:
            strategy = LinearMapping()

        elif mappingType == MappingType.ZIGZAG:
            strategy = ZigZagMapping()

        elif mappingType == MappingType.SERPENTINE:
            strategy = SerpentineMapping()

        return strategy.createImage(byteData)

    def __readBytes(self, filePath):

        with open(filePath, "rb") as file:
            return file.read()