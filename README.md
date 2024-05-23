# MTUOC-PCorpus-rescorer
A set of programs to rescore parallel corpora developed in the framework of the project **TAN-IBE: Neural Machine Translation for the romance languages of the Iberian Peninsula**, founded by the Spanish Ministry of Science and Innovation Proyectos de generación de conocimiento 2021. Reference: PID2021-124663OB-I00 founded by MCIN /AEI /10.13039/501100011033 / FEDER, UE.

## Prerequisites

By default, the program uses the fasttext language identification model [lid.176.bin](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin). You should download this model to the same directory of the programs. You may use any other fastext language identification model and even train your own model, as explained below.

The file requirements.txt have the requirements to install in order to run the programs.

## MTUOC-PCorpus-rescorer.py

This program creates a SQLite database storing the following information:

* source: the source segment
* target: the target segment
* score: for those corpora with a confidence score, as CCMatrix, for example, this confidence score is stored in this field.
* L1: the source language code detected by fasttext
* confL1: the language detection confidence for source language
* L2: the target language code detected by fasttext
* confL2: the language detection confidence for target language
* cosine_score: the cosine similarity between source and target segments.

We can get the helo of the program with option -h:

```
python3 MTUOC-PCorpus-rescorer.py -h
usage: MTUOC-PCorpus-rescorer.py [-h] -i INPUT -d DATABASE [-SEmodel SEMODEL] [-LDmodel LDMODEL]

MTUOC-PCorpus-rescorer: a script to score parallel corpora. The parallel corpus file should be a TSV file with source
segment, target segment and, optionally, a score. It creates a Sqlite database that should be used with the companion
program MTUOC-PCorpus-selector.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input parallel corpus file.
  -d DATABASE, --database DATABASE
                        The SQLITE database file.
  -SEmodel SEMODEL      The SentenceTransformer model. Default model: LaBSE
  -LDmodel LDMODEL      The fasttext language detection model. Default model: lid.176.bin
```


