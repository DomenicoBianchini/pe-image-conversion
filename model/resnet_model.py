import torch
import torch.nn as nn
from transformers import ResNetForImageClassification
from sklearn.metrics import confusion_matrix

class ResNetModel:

    def __init__(self, modelPath=None):

        # device utilizzato dal modello
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # caricamento modello
        if modelPath is None:

            self.__model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50", num_labels=2, ignore_mismatched_sizes=True)

        else:

            self.__model = ResNetForImageClassification.from_pretrained(modelPath)

        # spostamento modello sul device
        self.__model.to(self.__device)

    def train(self, trainLoader, validationLoader, epochs, learningRate, modelPath):

        # funzione di loss
        criterion = nn.CrossEntropyLoss()

        # ottimizzatore
        optimizer = torch.optim.Adam(self.__model.parameters(), lr=learningRate)

        # valore iniziale per confronto validation loss
        bestValidationLoss = float("inf")

        for epoch in range(epochs):

            # modalità training
            self.__model.train()
            trainLoss = 0.0

            for images, labels in trainLoader:

                # spostamento dati sul device
                images = images.to(self.__device)
                labels = labels.to(self.__device)

                # azzeramento gradienti
                optimizer.zero_grad()

                # forward pass
                outputs = self.__model(images).logits

                # calcolo loss
                loss = criterion(outputs, labels)

                # backward pass
                loss.backward()

                # aggiornamento pesi
                optimizer.step()

                # accumulo loss del batch
                trainLoss += loss.item() * images.size(0)

            # media della loss di training
            trainLoss /= len(trainLoader.dataset)

            # validation dopo ogni epoca
            validationLoss = self.__validate(validationLoader, criterion)

            print("Epoca:", epoch + 1, "Train Loss:", trainLoss, "Validation Loss:", validationLoss)

            # salvataggio modello migliore
            if validationLoss < bestValidationLoss:

                bestValidationLoss = validationLoss
                self.__model.save_pretrained(modelPath)

    def __validate(self, validationLoader, criterion):

        # modalità evaluation
        self.__model.eval()
        validationLoss = 0.0

        with torch.no_grad():

            for images, labels in validationLoader:

                # spostamento dati sul device
                images = images.to(self.__device)
                labels = labels.to(self.__device)

                # predizione
                outputs = self.__model(images).logits

                # calcolo loss
                loss = criterion(outputs, labels)
                validationLoss += loss.item() * images.size(0)

        validationLoss /= len(validationLoader.dataset)

        return validationLoss

    def test(self, testLoader):

        # modalità evaluation
        self.__model.eval()

        trueLabels = []
        predictedLabels = []

        with torch.no_grad():

            for images, labels in testLoader:

                # spostamento immagini sul device
                images = images.to(self.__device)

                # predizione
                outputs = self.__model(images).logits
                predictions = outputs.argmax(dim=1)
                trueLabels.extend(labels.cpu().numpy())
                predictedLabels.extend(predictions.cpu().numpy())

        # creazione matrice di confusione
        matrix = confusion_matrix(trueLabels, predictedLabels)

        return matrix