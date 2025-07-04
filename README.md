# Influence Diffusion Benchmark Project

## Descrizione del Progetto

Questo progetto si propone di confrontare due algoritmi per la selezione del Seed Set iniziale all'interno di una rete sociale, con l'obiettivo di massimizzare la diffusione dell'influenza attraverso un modello di **Influence Diffusion**. Oltre a questi, è stato sviluppato un terzo algoritmo volto a migliorare le prestazioni dei metodi precedenti, e un quarto algoritmo, basato su una selezione casuale, utilizzato come baseline per evidenziare i limiti inferiori delle performance ottenibili.

L'analisi viene condotta rispettando un vincolo di budget `K`, ovvero la somma dei costi associati ai nodi selezionati come Seed Set non può eccedere tale valore.

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
pip install seaborn
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
- **src**: contiene il codice dell'algoritmo Cost-Seeds-Greedy scritto in linguaggio C
- **seedset.py**: contiene il codice dei 4 algoritmi usati per il confronto
- **requirements.txt**: contiene i requisiti necessari per avviare il progetto
- **influence.py**: contiene il codice dell'algoritmo di Influence Diffusion
- **cost-seeds-greedy.ipynb**: contiene la pipeline relativa all'esecuzione dell'algoritmo Cost-Seeds-Greedy
- **cost.py**: contiene le tre funzioni di costo utilizzate per il confronto
- **compare.ipynb**: contiene il codice per la generazione di grafici mettendo in evidenza le differenze tra gli algoritmi
- **test.ipynb**: è il file principale per eseguire gli algoritmi sulle funzioni di costo.
- **influence.ipynb**: effettua il confronto tra gli algoritmi su varie metriche generando grafici ad hoc

## Contributi

Eventuali contributi o suggerimenti sono ben accetti. Aprire una issue o inviare una pull request per proporre modifiche e miglioramenti. É possibile anche implementare un nuovo algoritmo e modificare opportunamente il codice al fine di confrontarlo con i 4 algoritmi implementati.
