# Influence Diffusion Benchmark Project

## Descrizione del Progetto

Questo progetto mira a confrontare due algoritmi per la selezione del **Seed Set** iniziale in una rete sociale, allo scopo di massimizzare il numero di nodi influenzati tramite un algoritmo di **Influence Diffusion**. Inoltre, abbiamo proposto un terzo algoritmo con l'intento di migliorare i risultati ottenuti dai metodi precedenti.

L'analisi viene condotta rispettando un vincolo di budget `K`, ovvero la somma dei costi associati ai nodi selezionati come seed set non può eccedere tale valore.

* **Rete utilizzata:**

  * Social Network di utenti **LastFTM** (7.624 nodi e 27.806 edges)
  * Fonte: [LastFM Asia Social Network](https://snap.stanford.edu/data/feather-lastfm-social.html)

## Obiettivi

* Confrontare l'efficacia degli algoritmi tramite metriche quali numero di nodi influenzati e rapidità della diffusione.
* Valutazione critica delle performance del nuovo algoritmo proposto rispetto agli altri due algoritmi.

## Come utilizzare il Progetto

1. Clonare la repository

```bash
git clone https://github.com/daqh/influence_diffusion_benchmark.git
```

2. Installare le dipendenze necessarie, come:
 ```bash
pip install networkx
pip install tqdm
```

3. Scarica il file **lastfm_asia_edges.csv** dalla Fonte e inseriscilo nel path corretto ("data/processed/")

4. Come prima riga del file.csv inserisci
```bash
node_1,node_2
```

5. Avviare le simulazioni desiderate modificando le variabili globali per selezionare algoritmo e funzione di costo. Esempio:
```bash
DATASET_NAME = "lastfm_asia"
SS_STRATEGY = "wtss"
COST_FN = "uniform"
NUM_STEPS = 30
```


## Struttura della Repository


## Contributi

Eventuali contributi o suggerimenti sono ben accetti. Aprire una issue o inviare una pull request per proporre modifiche e miglioramenti.
