import numpy as np

from .image import Image
from .image_mapping_strategy import ImageMappingStrategy

class ZigZagMapping(ImageMappingStrategy):

    def createImage(self, byteData):

        # inizializzazione del tensore immagine usando altezza, larghezza e numero di canali impostati
        image = np.zeros(
            (
                self.height,
                self.width,
                self.numberOfChannels
            ),
            dtype=np.uint8
        )

        index = 0

        # mappatura zigzag dei byte con percorrenza alternata delle righe
        for y in range(self.height):

            if y % 2 == 0:
                xRange = range(self.width)
            else:
                xRange = range(self.width - 1, -1, -1)

            for x in xRange:
                for c in range(self.numberOfChannels):

                    if index < len(byteData):
                        image[y][x][c] = byteData[index]
                        index += 1
                        
        return Image(image)