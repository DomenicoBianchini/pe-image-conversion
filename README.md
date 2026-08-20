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
  Contiene le impostazioni utilizzate per trasformare i file PE in immagini. Qui vengono indicati la cartella dei file da convertire, il file con le label, la cartella di destinazione delle immagini e il file CSV che associa ogni immagine alla relativa label. È inoltre possibile scegliere la strategia di mapping (`LINEAR`, `ZIGZAG` o `SERPENTINE`), la dimensione dell'immagine e il numero di canali. Se `height` è impostato a `0`, l'altezza viene calcolata in base ai dati del file; altrimenti viene utilizzata un'immagine di dimensioni fisse. I parametri `resizeWidth` e `resizeHeight` servono per ridimensionare le immagini prima del training. Impostandone almeno uno a `0`, il ridimensionamento viene disabilitato.  
  Il parametro `enabled` permette di decidere se eseguire oppure saltare questa fase.

- `TRAIN_CONFIGURATION`  
  Contiene le impostazioni per addestrare il modello ResNet. In questa sezione vengono indicati il file CSV con il mapping tra immagini e label, il numero di epoche, il learning rate e la cartella in cui salvare il modello migliore.  
  Il parametro `enabled` permette di decidere se avviare oppure saltare la fase di training.

- `TEST_CONFIGURATION`  
  Contiene le impostazioni per testare un modello già addestrato. Qui vengono indicati il file CSV con il mapping tra immagini e label del test, il percorso del modello da utilizzare e il file CSV in cui salvare i risultati delle metriche.  
  Il parametro `enabled` permette di decidere se eseguire oppure saltare la fase di test.

## Esecuzione

Dopo aver installato le dipendenze e modificato `config.ini`, il programma può essere avviato con:

```bash
python main/application.py
```

Le fasi della pipeline vengono eseguite in base al valore di `enabled` presente nelle rispettive sezioni del file di configurazione.

## Pipeline

Il progetto è composto da tre fasi principali:

1. I file PE vengono trasformati in immagini usando la strategia di mapping scelta.
2. Le immagini vengono utilizzate per addestrare il modello ResNet.
3. Il modello addestrato viene testato e le metriche vengono salvate in un file CSV.

Le fasi possono essere eseguite separatamente, abilitando solo quella necessaria.

## Formato dei dati

Il file CSV contenente le label dei file PE deve avere le colonne `filename` e `label`:

```csv
filename,label
sample.exe,1
```

Il programma genera un secondo file CSV con il percorso delle immagini e le relative label. Questo file deve avere le colonne `imagePath` e `label`:

```csv
imagePath,label
images/sample.exe.png,1
```

## Risultati

Le immagini convertite vengono salvate nella cartella indicata da `imagesPath` e il relativo file CSV nel percorso indicato da `imageLabelsPath`.

I modelli addestrati vengono salvati nella cartella indicata da `modelPath`. I risultati dei test, comprese le metriche di classificazione e la configurazione utilizzata, vengono aggiunti al file CSV indicato da `resultsPath`.