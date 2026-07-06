import torch
import torch.utils.data
from dataloader.image_dataset import ImageDataset

class DataLoader:

    def buildDataLoader(self, imageMapping, needResize, resizeWidth, resizeHeight):

        # creazione dataset partendo dal CSV con imagePath e label
        dataset = ImageDataset(imageMapping, needResize, resizeWidth, resizeHeight)

        # creazione DataLoader PyTorch
        dataLoader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

        # stampa controllo numero campioni
        print("Numero di campioni:", len(dataset))

        # stampa controllo dimensioni batch
        for images, labels in dataLoader:

            print("Batch immagini:", images.shape)
            print("Batch label:", labels.shape)
            break

        return dataLoader