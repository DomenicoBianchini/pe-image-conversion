import csv

class LabelDictionary:

    def __init__(self, labelsPath):

        # dizionario che associa il nome del file PE alla sua label
        self.__labelDictionary = {}

        # dizionario che associa il path dell'immagine alla sua label
        self.__imageDictionary = {}

        # lettura del file CSV contenente le label dei file PE
        with open(labelsPath, "r", newline="") as file:

            reader = csv.DictReader(file)

            # salvataggio del dizionario che associa il nome del file PE alla sua label
            for row in reader:

                self.__labelDictionary[row["filename"]] = int(row["label"])

    def addLabelImage(self, fileName, imagePath):

        # recupero della label associata al file PE
        label = self.__labelDictionary[fileName]

        # aggiunta del path dell'immagine e della sua label al dizionario
        self.__imageDictionary[imagePath] = label

    def save(self, imageLabelsPath):

        # apertura del file CSV per il salvataggio del mapping immagini-label
        with open(imageLabelsPath, "w", newline="") as file:
            writer = csv.writer(file)

            # scrittura dell'intestazione del file CSV
            writer.writerow(["imagePath", "label"])

            # scrittura del mapping del path dell'immagine e della sua label nel file CSV
            for imagePath, label in self.__imageDictionary.items():
                writer.writerow([imagePath, label])