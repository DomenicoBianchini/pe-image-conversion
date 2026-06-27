import numpy as np

from .image import Image
from .image_mapping_strategy import ImageMappingStrategy

class SerpentineMapping(ImageMappingStrategy):

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

        # mappatura serpentina dei byte con percorrenza diagonale alternata
        for diagonal in range(height + width - 1):

            positions = []

            startY = max(0, diagonal - (width - 1))
            endY = min(height - 1, diagonal)

            for y in range(startY, endY + 1):
                x = diagonal - y
                positions.append((y, x))

            if diagonal % 2 == 1:
                positions.reverse()

            for y, x in positions:
                for c in range(numberOfChannels):

                    if index < len(byteData):
                        image[y][x][c] = byteData[index]
                        index += 1

        return Image(image)