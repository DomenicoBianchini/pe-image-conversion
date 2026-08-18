import numpy as np

from .image import Image
from .image_mapping_strategy import ImageMappingStrategy

class SerpentineMapping(ImageMappingStrategy):

    def createImage(self, byteData):

        width = self.getWidth()
        height = self.getHeight()
        numberOfChannels = self.getNumberOfChannels()

        if height == 0:
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

        # mappatura serpentina dei byte con percorrenza diagonale alternata
        for diagonal in range(height + width - 1):

            startY = max(0, diagonal - (width - 1))
            endY = min(height - 1, diagonal)

            if diagonal % 2 == 0:
                yRange = range(startY, endY + 1)
            else:
                yRange = range(endY, startY - 1, -1)

            for y in yRange:

                x = diagonal - y

                for c in range(numberOfChannels):

                    if index < len(byteData):
                        image[y][x][c] = byteData[index]
                        index += 1

        return Image(image)