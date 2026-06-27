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

I parametri per la conversione sono impostati nel file:

`config.ini`

Nel file di configurazione è possibile modificare il percorso della cartella dei file PE, la strategia di mapping, le dimensioni dell'immagine e il numero di canali.

## Avvio

Per avviare il programma, dalla cartella principale del progetto eseguire:

```bash
python -m main.application
```
