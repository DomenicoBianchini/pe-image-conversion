import configparser

from pe.pe_file import PEFile
from pe.mapping_type import MappingType
from image_representation.image_mapping_strategy import ImageMappingStrategy

class Application:

    def parseConfig(self, configPath):

        # lettura del file di configurazione
        config = configparser.ConfigParser()
        config.read(configPath)

        settings = config["IMAGE_CONFIGURATION"]
        peFilePath = settings["peFilePath"]
        mappingType = MappingType(settings["mappingType"])
        width = int(settings["width"])
        numberOfChannels = int(settings["numberOfChannels"])
        height = None

        # se height è vuota viene lasciata None per la modalità variable
        if settings.get("height"):
            height = int(settings["height"])

        # configurazione delle dimensioni e del numero di canali per il mapping
        ImageMappingStrategy.setImageSize(width,height,numberOfChannels)

        peFile = PEFile()

        # lettura del file PE e creazione dell'immagine corrispondente
        image = peFile.read(peFilePath,mappingType)

        if image.getNumberOfChannels() == 1:
            channelType = "GRAY"
        else:
            channelType = "RGB"

        imageSize = str(image.getWidth()) + "x" + str(image.getHeight())

        # salvataggio dell'immagine con un nome che indica il mapping, il tipo di canali e le dimensioni
        fileName = "output/" + mappingType.name + "_" + channelType + "_" + imageSize + ".png"

        image.save(fileName)


if __name__ == "__main__":

    application = Application()
    application.parseConfig("config.ini")