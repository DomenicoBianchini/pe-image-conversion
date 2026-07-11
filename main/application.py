import configparser
import os

from pe.pe_file import PEFile
from pe.mapping_type import MappingType
from image_representation.image_mapping_strategy import ImageMappingStrategy
from dataloader.data_loader import DataLoader
from model.resnet_model import ResNetModel

class Application:

    def __parseConfig(self, configPath):

        config = configparser.ConfigParser()
        config.read(configPath)

        # lettura configurazione della parte di conversione PE -> immagini
        imageConfig = config["IMAGE_CONFIGURATION"]

        # flag per abilitare la parte di conversione PE -> immagini
        self.peEnabled = int(imageConfig["enabled"])

        # parametri della parte di conversione PE -> immagini
        self.filesPath = imageConfig["filesPath"]
        self.labelsPath = imageConfig["labelsPath"]
        self.imagePath = imageConfig["imagePath"]
        self.imageMapping = imageConfig["imageMapping"]
        self.mappingType = MappingType(imageConfig["mappingType"])
        self.width = int(imageConfig["width"])
        self.height = int(imageConfig["height"])
        self.numberOfChannels = int(imageConfig["numberOfChannels"])

        # lettura configurazione della parte di training
        trainConfig = config["TRAIN_CONFIGURATION"]

        # flag per abilitare la parte di training
        self.trainEnabled = int(trainConfig["enabled"])

        # dimensioni del resize
        self.resizeWidth = int(trainConfig["resizeWidth"])
        self.resizeHeight = int(trainConfig["resizeHeight"])

    def main(self):

        # lettura del file di configurazione
        self.__parseConfig("config.ini")

        # esecuzione pipeline conversione PE
        if self.peEnabled == 1:

            # configurazione delle dimensioni e del numero di canali per il mapping
            ImageMappingStrategy.setImageSize(self.width, self.height, self.numberOfChannels)

            # avvio lettura file PE e generazione immagini
            peFile = PEFile()

            # lettura di tutti i file PE presenti nella cartella
            for fileName in os.listdir(self.filesPath):
                
                filePath = os.path.join(self.filesPath, fileName)

                # conversione del file PE in immagine
                peFile.PEToImage(filePath, self.imagePath, self.mappingType)

        # esecuzione pipeline di training
        if self.trainEnabled == 1:

            # verifica se è necessario effettuare il resize delle immagini
            if self.resizeHeight != 0:
                needResize = True
            else:
                needResize = False

            # costruzione dataset e DataLoader
            dataLoader = DataLoader()
            imageDataloader = dataLoader.buildDataLoader(self.imageMapping, needResize, self.resizeWidth, self.resizeHeight)

            # ResNet modello preaddestrato
            resnet = ResNetModel()
            for images, labels in imageDataloader:
                resnet.predict(images)
                break

if __name__ == "__main__":

    app = Application()
    app.main()