import torch
from transformers import AutoImageProcessor, ResNetForImageClassification

class ResNetModel:

    def __init__(self):

        # processor preaddestrato
        self.__processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")

        # modello preaddestrato
        self.__model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

        # modalità evaluation
        self.__model.eval()

    def predict(self, images):

        # preprocessing delle immagini
        inputs = self.__processor(images, return_tensors="pt", do_resize=False, do_center_crop=False, do_rescale=True, do_normalize=True)

        with torch.no_grad():
            logits = self.__model(**inputs).logits

        # predizioni delle label
        predicted_indexes = logits.argmax(-1)
        for idx in predicted_indexes:
            print(self.__model.config.id2label[idx.item()])