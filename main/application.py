import configparser

from pe.pe_file import PEFile
from pe.mapping_type import MappingType
from image_representation.image_mapping_strategy import ImageMappingStrategy

class Application:

    def parseConfig(self, configPath):

        config = configparser.ConfigParser()
        config.read(configPath)

        settings = config["IMAGE_CONFIGURATION"]
        peFilePath = settings["peFilePath"]
        mappingType = MappingType(settings["mappingType"])
        width = int(settings["width"])
        numberOfChannels = int(settings["numberOfChannels"])
        height = None
        if settings.get("height"):
            height = int(settings["height"])

        ImageMappingStrategy.setImageSize(
            width,
            height,
            numberOfChannels
        )

        peFile = PEFile()

        image = peFile.read(
            peFilePath,
            mappingType
        )
        
        if image.getNumberOfChannels() == 1:
            colorMode = "GRAY"
        else:
            colorMode = "RGB"

        imageSize = str(image.getWidth()) + "x" + str(image.getHeight())
        fileName = "output/" + mappingType.name + "_" + colorMode + "_" + imageSize + ".png"

        image.save(fileName)


if __name__ == "__main__":

    application = Application()
    application.parseConfig("config.ini")