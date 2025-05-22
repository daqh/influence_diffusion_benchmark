# Influence Diffusion Benchmark Project

## Descrizione del Progetto

Questo progetto mira a confrontare due algoritmi per la selezione del **Seed Set** iniziale in una rete sociale, allo scopo di massimizzare il numero di nodi influenzati tramite un algoritmo di **Influence Diffusion**. Inoltre, abbiamo proposto un terzo algoritmo con l'intento di migliorare i risultati ottenuti dai metodi precedenti.

L'analisi viene condotta rispettando un vincolo di budget `K`, ovvero la somma dei costi associati ai nodi selezionati come seed set non può eccedere tale valore.

* **Rete utilizzata:**

  * Graph Embedding with Self Clustering: Facebook (34.833 nodi e 1.380.293 edges)
  * Fonte: [Gemsec Facebook dataset](https://snap.stanford.edu/data/gemsec-Facebook.html)

## Obiettivi

* Confrontare l'efficacia degli algoritmi tramite metriche quali numero di nodi influenzati e rapidità della diffusione.
* Valutazione critica delle performance del nuovo algoritmo proposto rispetto agli altri due algoritmi.

## Come utilizzare il Progetto

1. Clonare la repository

```bash
git clone https://github.com/yourusername/yourrepository.git
```

2. Installare le dipendenze necessarie

3. Eseguire gli script per la selezione del seed set

4. Avviare la simulazione di diffusione

## Struttura della Repository


## Contributi

Eventuali contributi o suggerimenti sono ben accetti. Aprire una issue o inviare una pull request per proporre modifiche e miglioramenti.
