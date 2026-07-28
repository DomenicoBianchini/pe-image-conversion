import torch
import torch.nn as nn
from transformers import ResNetForImageClassification
from sklearn.metrics import confusion_matrix

class ResNetModel:

    def __init__(self, modelPath=None):

        # seed per la riproducibilità
        SEED = 42
        torch.manual_seed(SEED)
        torch.cuda.manual_seed_all(SEED)

        # device utilizzato dal modello
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # caricamento modello
        if modelPath is None:

            self.__model = ResNetForImageClassification.from_pretrained(
                "microsoft/resnet-50",
                num_labels=2,
                id2label={0: "goodware", 1: "malware"},
                label2id={"goodware": 0, "malware": 1},
                ignore_mismatched_sizes=True
            )

        else:

            self.__model = ResNetForImageClassification.from_pretrained(modelPath)

        # utilizzo di tutte le GPU disponibili
        if torch.cuda.device_count() > 1:

            print("GPU disponibili:", torch.cuda.device_count())

            self.__model = nn.DataParallel(self.__model)

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

            for batch, (images, labels) in enumerate(trainLoader, start=1):

                # spostamento dati sul device
                images = images.to(self.__device, non_blocking=True)
                labels = labels.to(self.__device, non_blocking=True)

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

                if batch % 1000 == 0:

                    print(f"Epoca: {epoch + 1} | Batch: {batch}/{len(trainLoader)}")

            # media della loss di training
            trainLoss /= len(trainLoader.dataset)

            # validation dopo ogni epoca
            validationLoss = self.__validate(validationLoader, criterion)

            print(f"Epoca: {epoch + 1} | Train Loss: {trainLoss:.4f} | Validation Loss: {validationLoss:.4f}")

            # salvataggio modello migliore
            if validationLoss < bestValidationLoss:

                bestValidationLoss = validationLoss

                # salvataggio del modello
                if isinstance(self.__model, nn.DataParallel):

                    self.__model.module.save_pretrained(modelPath)

                else:

                    self.__model.save_pretrained(modelPath)

    def __validate(self, validationLoader, criterion):

        # modalità evaluation
        self.__model.eval()
        validationLoss = 0.0

        with torch.no_grad():

            for images, labels in validationLoader:

                # spostamento dati sul device
                images = images.to(self.__device, non_blocking=True)
                labels = labels.to(self.__device, non_blocking=True)

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
                images = images.to(self.__device, non_blocking=True)

                # predizione
                outputs = self.__model(images).logits
                predictions = outputs.argmax(dim=1)

                trueLabels.extend(labels.cpu().numpy())
                predictedLabels.extend(predictions.cpu().numpy())

        # creazione matrice di confusione
        matrix = confusion_matrix(trueLabels, predictedLabels)

        return matrix