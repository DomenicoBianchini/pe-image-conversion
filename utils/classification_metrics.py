import csv
import os

class ClassificationMetrics:

    def __init__(self, confusionMatrix):

        # lettura dei valori della matrice di confusione
        self.__trueNegative, self.__falsePositive, self.__falseNegative, self.__truePositive = confusionMatrix.flatten()

        # inizializzazione delle metriche
        self.__precisionGoodware = 0
        self.__recallGoodware = 0
        self.__f1Goodware = 0
        self.__precisionMalware = 0
        self.__recallMalware = 0
        self.__f1Malware = 0
        self.__overallAccuracy = 0

    def calculateMetrics(self):

        # calcolo della precision per la classe goodware
        self.__precisionGoodware = self.__trueNegative / (self.__trueNegative + self.__falseNegative)

        # calcolo della recall per la classe goodware
        self.__recallGoodware = self.__trueNegative / (self.__trueNegative + self.__falsePositive)

        # calcolo della F1-score per la classe goodware
        self.__f1Goodware = 2 * self.__precisionGoodware * self.__recallGoodware / (self.__precisionGoodware + self.__recallGoodware)

        # calcolo della precision per la classe malware
        self.__precisionMalware = self.__truePositive / (self.__truePositive + self.__falsePositive)

        # calcolo della recall per la classe malware
        self.__recallMalware = self.__truePositive / (self.__truePositive + self.__falseNegative)

        # calcolo della F1-score per la classe malware
        self.__f1Malware = 2 * self.__precisionMalware * self.__recallMalware / (self.__precisionMalware + self.__recallMalware)

        # calcolo dell'overall accuracy
        self.__overallAccuracy = (self.__trueNegative + self.__truePositive) / (
            self.__trueNegative +
            self.__falsePositive +
            self.__falseNegative +
            self.__truePositive
        )

    def save(self, resultsPath, configuration):

        # verifica se la cartella del file CSV esiste
        directory = os.path.dirname(resultsPath)

        if directory != "":
            os.makedirs(directory, exist_ok=True)

        # verifica se il file CSV esiste già
        fileExists = os.path.exists(resultsPath)

        # apertura del file CSV in modalità append
        with open(resultsPath, "a", newline="") as file:

            # creazione del writer CSV
            writer = csv.writer(file)

            # scrittura dell'intestazione se il file non esiste
            if not fileExists:

                writer.writerow([
                    "mappingType",
                    "width",
                    "height",
                    "numberOfChannels",
                    "resize",
                    "epochs",
                    "learningRate",
                    "TN",
                    "FP",
                    "FN",
                    "TP",
                    "overall_accuracy",
                    "precision_goodware",
                    "recall_goodware",
                    "f1_goodware",
                    "precision_malware",
                    "recall_malware",
                    "f1_malware"
                ])

            # conversione dei valori di configurazione per il CSV
            if configuration["height"] == 0:
                height = "VARIABLE"
            else:
                height = configuration["height"]

            if configuration["resizeWidth"] == 0 or configuration["resizeHeight"] == 0:
                resize = "NO_RESIZE"
            else:
                resize = str(configuration["resizeWidth"]) + "x" + str(configuration["resizeHeight"])

            # scrittura dei risultati della configurazione
            writer.writerow([
                configuration["mappingType"],
                configuration["width"],
                height,
                configuration["numberOfChannels"],
                resize,
                configuration["epochs"],
                configuration["learningRate"],
                self.__trueNegative,
                self.__falsePositive,
                self.__falseNegative,
                self.__truePositive,
                round(self.__overallAccuracy, 4),
                round(self.__precisionGoodware, 4),
                round(self.__recallGoodware, 4),
                round(self.__f1Goodware, 4),
                round(self.__precisionMalware, 4),
                round(self.__recallMalware, 4),
                round(self.__f1Malware, 4)
            ])