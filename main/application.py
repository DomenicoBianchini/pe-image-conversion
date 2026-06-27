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
        filesPath = settings["filesPath"]
        mappingType = MappingType(settings["mappingType"])
        width = int(settings["width"])
        numberOfChannels = int(settings["numberOfChannels"])
        height = None

        # se height è vuota viene lasciata None per la modalità variable
        if settings.get("height"):
            height = int(settings["height"])

        # configurazione delle dimensioni e del numero di canali per il mapping
        ImageMappingStrategy.setImageSize(width, height, numberOfChannels)

        peFile = PEFile()

        # lettura dei file PE e creazione delle immagini
        peFile.read(filesPath, mappingType)


if __name__ == "__main__":

    application = Application()
    application.parseConfig("config.ini")