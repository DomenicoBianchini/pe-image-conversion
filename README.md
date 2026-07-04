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

Il progetto utilizza un unico file di configurazione (`config.ini`), suddiviso in due sezioni:

- `IMAGE_CONFIGURATION`  
  Configura la fase di conversione dei file PE in immagini (cartella dei file PE, strategia di mapping, dimensioni dell'immagine e numero di canali).  
  Include inoltre un parametro `enabled` che abilita o disabilita l'esecuzione di questa fase della pipeline.

- `DATASET_CONFIGURATION`  
  Configura la fase di costruzione del dataset e del DataLoader (path del file CSV contenente il mapping immagini-label e parametri per il resize delle immagini).  
  Include inoltre un parametro `enabled` che abilita o disabilita l'esecuzione di questa fase della pipeline.