import numpy as np

from .image import Image
from .image_mapping_strategy import ImageMappingStrategy

class LinearMapping(ImageMappingStrategy):

    def createImage(self, byteData):

        width = self.getWidth()
        height = self.getHeight()
        numberOfChannels = self.getNumberOfChannels()

        if height is None:
            height = self.getVariableHeight(len(byteData))

        # inizializzazione del tensore immagine usando altezza, larghezza e numero di canali impostati
        image = np.zeros(
            (
                height,
                width,
                numberOfChannels
            ),
            dtype=np.uint8
        )

        index = 0

        # mappatura lineare sequenziale dei byte
        for y in range(height):
            for x in range(width):
                for c in range(numberOfChannels):

                    if index < len(byteData):
                        image[y][x][c] = byteData[index]
                        index += 1
                        
        return Image(image)