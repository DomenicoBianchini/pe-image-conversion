import torch
from torch.utils.data import random_split
from dataloader.image_dataset import ImageDataset

class DataLoader:

    def buildTrainValidationLoader(self, imageLabelsPath, needResize, resizeWidth, resizeHeight):

        # creazione dataset completo del training
        dataset = ImageDataset(imageLabelsPath, needResize, resizeWidth, resizeHeight)

        # divisione dataset in train e validation
        validationSize = int(0.2 * len(dataset))
        trainSize = len(dataset) - validationSize

        generator = torch.Generator().manual_seed(42)
        trainDataset, validationDataset = random_split(dataset, [trainSize, validationSize], generator=generator)

        # creazione DataLoader del training
        trainLoader = torch.utils.data.DataLoader(
            trainDataset,
            batch_size=32,
            shuffle=True,
            num_workers=2,
            pin_memory=True,
            prefetch_factor=1,
            persistent_workers=False
        )

        # creazione DataLoader della validation
        validationLoader = torch.utils.data.DataLoader(
            validationDataset,
            batch_size=32,
            shuffle=False,
            num_workers=2,
            pin_memory=True,
            prefetch_factor=1,
            persistent_workers=False
        )

        return trainLoader, validationLoader

    def buildTestLoader(self, imageLabelsPath, needResize, resizeWidth, resizeHeight):

        # creazione dataset del test
        dataset = ImageDataset(imageLabelsPath, needResize, resizeWidth, resizeHeight)

        # creazione DataLoader del test
        testLoader = torch.utils.data.DataLoader(
            dataset,
            batch_size=32,
            shuffle=False,
            num_workers=2,
            pin_memory=True,
            prefetch_factor=1,
            persistent_workers=False
        )

        return testLoader