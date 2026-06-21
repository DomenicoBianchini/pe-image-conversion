import numpy as np

from .image import Image
from .image_mapping_strategy import ImageMappingStrategy

class LinearMapping(ImageMappingStrategy):

    def createImage(self, byteData):

        image = np.zeros(
            (
                self.height,
                self.width,
                self.numberOfChannels
            ),
            dtype=np.uint8
        )

        index = 0

        for y in range(self.height):
            for x in range(self.width):
                for c in range(self.numberOfChannels):

                    if index < len(byteData):
                        image[y][x][c] = byteData[index]
                        index += 1
                        
        return Image(image)