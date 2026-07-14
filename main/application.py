import configparser
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils.csv_image_mapping import CSVImageMapping
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
        self.imagesPath = imageConfig["imagesPath"]
        self.imageMapping = imageConfig["imageMapping"]
        self.mappingType = MappingType(imageConfig["mappingType"])
        self.width = int(imageConfig["width"])
        self.height = int(imageConfig["height"])
        self.numberOfChannels = int(imageConfig["numberOfChannels"])

        # dimensioni resize immagini
        self.resizeWidth = int(imageConfig["resizeWidth"])
        self.resizeHeight = int(imageConfig["resizeHeight"])

        # lettura configurazione della parte di training
        trainConfig = config["TRAIN_CONFIGURATION"]

        # flag per abilitare la parte di training
        self.trainEnabled = int(trainConfig["enabled"])

        # parametri training
        self.trainImageMapping = trainConfig["imageMapping"]
        self.epochs = int(trainConfig["epochs"])
        self.learningRate = float(trainConfig["learningRate"])
        self.modelPath = trainConfig["modelPath"]

        # lettura configurazione della parte di test
        testConfig = config["TEST_CONFIGURATION"]

        # flag per abilitare la parte di test
        self.testEnabled = int(testConfig["enabled"])

        # parametri test
        self.testImageMapping = testConfig["imageMapping"]
        self.testModelPath = testConfig["modelPath"]
        self.confusionMatrixPath = testConfig["confusionMatrixPath"]

    def main(self):

        # lettura del file di configurazione
        self.__parseConfig("config.ini")

        # esecuzione pipeline conversione PE
        if self.peEnabled == 1:

            # configurazione delle dimensioni e del numero di canali per il mapping
            ImageMappingStrategy.setImageSize(self.width, self.height, self.numberOfChannels)

            # creazione oggetto per la conversione dei file PE in immagini
            peFile = PEFile()

            # creazione oggetto per la gestione del file CSV contenente il mapping immagini-label
            csvImageMapping = CSVImageMapping()

            # lettura del mapping file-label dal CSV
            labelMapping = csvImageMapping.loadLabelMapping(self.labelsPath)

            # creazione del file CSV contenente il mapping immagini-label
            mappingFile, writer = csvImageMapping.createImageMapping(self.imageMapping)

            # lettura di tutti i file PE presenti nella cartella
            for fileName in os.listdir(self.filesPath):

                filePath = os.path.join(self.filesPath, fileName)

                peFile.PEToImage(filePath, self.imagesPath, self.mappingType)

                # recupero della label del file PE
                label = labelMapping[fileName]

                # path dell'immagine generata
                imagePath = os.path.join(self.imagesPath, fileName + ".png")

                # salvataggio del mapping immagine-label
                csvImageMapping.addImageMapping(writer, imagePath, label)

            # chiusura del file CSV
            mappingFile.close()

        # verifica se è necessario effettuare il resize delle immagini
        if self.resizeHeight != 0:
            needResize = True
        else:
            needResize = False

        # esecuzione pipeline di training
        if self.trainEnabled == 1:

            # costruzione DataLoader train e validation
            dataLoader = DataLoader()
            trainLoader, validationLoader = dataLoader.buildTrainValidationLoader(self.trainImageMapping, needResize, self.resizeWidth, self.resizeHeight)

            # creazione modello ResNet
            resnet = ResNetModel()

            # avvio training
            resnet.train(trainLoader, validationLoader, self.epochs, self.learningRate, self.modelPath)

        # esecuzione pipeline di test
        if self.testEnabled == 1:

            # costruzione DataLoader test
            dataLoader = DataLoader()
            testLoader = dataLoader.buildTestLoader(self.testImageMapping, needResize, self.resizeWidth, self.resizeHeight)

            # caricamento modello salvato
            resnet = ResNetModel(self.testModelPath)

            # esecuzione test
            matrix = resnet.test(testLoader)

            # salvataggio matrice di confusione
            sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues",
                        cbar=False, xticklabels=["Goodware", "Malware"],
                        yticklabels=["Goodware", "Malware"])
            plt.xlabel("Predicted")
            plt.ylabel("Actual")
            plt.title("Confusion Matrix")
            plt.savefig(self.confusionMatrixPath)

if __name__ == "__main__":

    app = Application()
    app.main()