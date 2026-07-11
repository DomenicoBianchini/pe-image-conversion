import csv

class CSVImageMapping:

    def loadLabelMapping(self, labelsPath):

        labelMapping = {}

        # lettura del file CSV contenente le label dei file PE
        with open(labelsPath, "r", newline="") as file:

            reader = csv.DictReader(file)

            # salvataggio della label associata a ciascun file PE
            for row in reader:

                if row["list"] == "Whitelist":
                    labelMapping[row["id"]] = 0

                elif row["list"] == "Blacklist":
                    labelMapping[row["id"]] = 1

        return labelMapping

    def createImageMapping(self, imageMapping):

        # creazione del file CSV contenente il mapping immagini-label
        file = open(imageMapping, "w", newline="")

        writer = csv.writer(file)

        # intestazione del file CSV
        writer.writerow(["imagePath", "label"])

        return file, writer

    def addImageMapping(self, writer, imagePath, label):

        # aggiunta di una nuova immagine con la relativa label
        writer.writerow([imagePath, label])