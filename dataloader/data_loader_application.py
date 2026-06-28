import configparser
from torch.utils.data import DataLoader

from dataloader.image_dataset import ImageDataset

class DataLoaderApplication:

    def parseConfig(self, configPath):

        # lettura del file di configurazione
        config = configparser.ConfigParser()
        config.read(configPath)

        imagesPath = config["DATASET"]["imagesPath"]
        labelsPath = config["DATASET"]["labelsPath"]

        self.buildDataLoader(imagesPath, labelsPath)


    def buildDataLoader(self, imagesPath, labelsPath):

        # creazione del Dataset
        dataset = ImageDataset(imagesPath, labelsPath)

        # creazione del DataLoader
        dataLoader = DataLoader(dataset, batch_size=32, shuffle=True)

        print("Numero di campioni:", len(dataset))

        # prova di caricamento del primo batch
        for images, labels in dataLoader:
            print("Batch immagini:", images.shape)
            print("Batch label:", labels.shape)
            break


if __name__ == "__main__":

    application = DataLoaderApplication()
    application.parseConfig("dl_config.ini")