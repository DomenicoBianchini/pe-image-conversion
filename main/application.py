import configparser
import json
import os

from utils.classification_metrics import ClassificationMetrics
from utils.label_dictionary import LabelDictionary
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
        self.peEnabled = imageConfig["enabled"] == "1"

        # parametri della parte di conversione PE -> immagini
        self.filesPath = imageConfig["filesPath"]
        self.labelsPath = imageConfig["labelsPath"]
        self.imagesPath = imageConfig["imagesPath"]
        self.imageLabelsPath = imageConfig["imageLabelsPath"]
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
        self.trainEnabled = trainConfig["enabled"] == "1"

        # parametri training
        self.trainImageLabelsPath = trainConfig["imageLabelsPath"]
        self.epochs = int(trainConfig["epochs"])
        self.learningRate = float(trainConfig["learningRate"])
        self.modelPath = trainConfig["modelPath"]

        # lettura configurazione della parte di test
        testConfig = config["TEST_CONFIGURATION"]

        # flag per abilitare la parte di test
        self.testEnabled = testConfig["enabled"] == "1"

        # parametri test
        self.testImageLabelsPath = testConfig["imageLabelsPath"]
        self.testModelPath = testConfig["modelPath"]
        self.resultsPath = testConfig["resultsPath"]

    def main(self):

        # lettura del file di configurazione
        self.__parseConfig("config.ini")

        # esecuzione pipeline conversione PE
        if self.peEnabled:

            # configurazione delle dimensioni e del numero di canali per il mapping
            ImageMappingStrategy.setImageSize(self.width, self.height, self.numberOfChannels)

            # creazione oggetto per la conversione dei file PE in immagini
            peFile = PEFile()

            # creazione oggetto per la gestione delle label e del mapping immagini-label
            labelDictionary = LabelDictionary(self.labelsPath)

            # lettura di tutti i file PE presenti nella cartella
            for fileName in os.listdir(self.filesPath):

                filePath = os.path.join(self.filesPath, fileName)

                # conversione del file PE in immagine
                peFile.PEToImage(filePath, self.imagesPath, self.mappingType)

                # path dell'immagine generata
                imagePath = os.path.join(self.imagesPath, fileName + ".png")

                # aggiunta del path dell'immagine e della sua label al dizionario
                labelDictionary.addLabelImage(fileName, imagePath)

            # salvataggio del CSV contenente il mapping fra il path delle immagini e le relative label
            labelDictionary.save(self.imageLabelsPath)

        # verifica se è necessario effettuare il resize delle immagini
        if self.resizeWidth == 0 or self.resizeHeight == 0:
            needResize = False
        else:
            needResize = True

        # esecuzione pipeline di training
        if self.trainEnabled:

            # costruzione DataLoader train e validation
            dataLoader = DataLoader()
            trainLoader, validationLoader = dataLoader.buildTrainValidationLoader(self.trainImageLabelsPath, needResize, self.resizeWidth, self.resizeHeight)

            # creazione modello ResNet
            resnet = ResNetModel()

            # costruzione del nome delle dimensioni
            if self.height == 0:
                imageSize = str(self.width) + "xVARIABLE"
            else:
                imageSize = str(self.width) + "x" + str(self.height)

            # identificazione del numero di canali
            if self.numberOfChannels == 1:
                channels = "GRAY"
            else:
                channels = "RGB"

            # costruzione del nome della configurazione delle immagini
            configurationName = self.mappingType.value + "_" + imageSize + "_" + channels

            # costruzione del nome della configurazione del resize
            if self.resizeWidth == 0 or self.resizeHeight == 0:
                resizeName = "NO_RESIZE"
            else:
                resizeName = "RESIZE_" + str(self.resizeWidth) + "x" + str(self.resizeHeight)

            # costruzione del nome della configurazione del training
            trainingName = "EPOCHS_" + str(self.epochs) + "_LR_" + str(self.learningRate) + "_" + resizeName

            # costruzione del path del modello
            modelPath = os.path.join(self.modelPath, configurationName, trainingName)

            # avvio training
            resnet.train(trainLoader, validationLoader, self.epochs, self.learningRate, modelPath)

            # configurazione utilizzata per il training
            configuration = {
                "mappingType": self.mappingType.value,
                "width": self.width,
                "height": self.height,
                "numberOfChannels": self.numberOfChannels,
                "resizeWidth": self.resizeWidth,
                "resizeHeight": self.resizeHeight,
                "epochs": self.epochs,
                "learningRate": self.learningRate
            }

            # path del file contenente la configurazione
            configurationPath = os.path.join(modelPath, "training_configuration.json")

            # salvataggio della configurazione
            with open(configurationPath, "w") as file:
                json.dump(configuration, file, indent=4)

        # esecuzione pipeline di test
        if self.testEnabled:

            # costruzione DataLoader test
            dataLoader = DataLoader()
            testLoader = dataLoader.buildTestLoader(self.testImageLabelsPath, needResize, self.resizeWidth, self.resizeHeight)

            # caricamento modello salvato
            resnet = ResNetModel(self.testModelPath)

            # esecuzione del test
            matrix = resnet.test(testLoader)

            # creazione oggetto per il calcolo delle metriche
            classificationMetrics = ClassificationMetrics(matrix)

            # calcolo delle metriche
            classificationMetrics.calculateMetrics()

            # lettura della configurazione utilizzata per il training del modello
            configurationPath = os.path.join(self.testModelPath, "training_configuration.json")

            with open(configurationPath, "r") as file:
                configuration = json.load(file)

            # salvataggio dei risultati del test con la configurazione del modello testato
            classificationMetrics.save(self.resultsPath, configuration)


if __name__ == "__main__":

    app = Application()
    app.main()