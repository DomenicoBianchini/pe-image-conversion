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

I parametri sono divisi in due file di configurazione:

- `pe_config.ini`
	Configura la conversione dei file PE in immagini (cartella dei PE, strategia di mapping, dimensioni immagine, numero di canali).

- `dl_config.ini`
	Configura il caricamento del dataset immagini (path cartella immagini e path file CSV delle label).