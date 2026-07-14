# PE Image Conversion

Progetto per la conversione di file PE (Portable Executable) Windows in immagini tramite diverse strategie di mapping:

- LINEAR
- ZIGZAG
- SERPENTINE

## Installazione

Installare le librerie necessarie con:

```bash
pip install -r requirements.txt
```

## Configurazione

Il progetto utilizza un unico file di configurazione (`config.ini`), suddiviso in tre sezioni:

- `IMAGE_CONFIGURATION`  
  Configura la fase di conversione dei file PE in immagini (cartella dei file PE, file CSV con le label, cartella di salvataggio delle immagini, file CSV di mapping immagini-label, strategia di mapping, dimensioni dell'immagine e il numero di canali).  
  Include inoltre un parametro `enabled` che abilita o disabilita l'esecuzione di questa fase della pipeline.

- `TRAIN_CONFIGURATION`  
  Configura la fase di training della ResNet (file CSV contenente il mapping immagini-label del training, numero di epoche, learning rate e il percorso dove salvare il modello migliore).  
  Include inoltre un parametro `enabled` che abilita o disabilita l'esecuzione di questa fase della pipeline.

- `TEST_CONFIGURATION`  
  Configura la fase di test della ResNet (file CSV contenente il mapping immagini-label del test, percorso del modello salvato durante il training e il percorso dove salvare la matrice di confusione).  
  Include inoltre un parametro `enabled` che abilita o disabilita l'esecuzione di questa fase della pipeline.