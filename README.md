# PHERI

This is repository of Phage Host ExploRatIon tool.
The main purpose of this program is to predict phage hosts from sequence in FASTA format.
Currently we are able to predict 8 host genera with very high accuracy (around 97%).
These genera are Arthrobacter, Escherichia, Gordonia, Lactococcus, Mycobacterium, Pseudomonas, Staphylococcus, Streptococcus.

To install this tool please use our [docker image](https://hub.docker.com/r/andynet/pheri/).

PHERI uses preprocessed data stored in the folder [files](../../tree/master/files).
The whole preprocessing pipeline can be found [here](https://github.com/andynet/pheri_preprocessing).

The paper describing the method is available on [bioRxiv](https://www.biorxiv.org/content/10.1101/2020.05.13.093773v1.full).

To build the conda package:
'''
conda build purge
conda build -c conda-forge -c bioconda . 1>log 2>&1
'''


# Install

conda create -n test
conda install -c bioconda -c conda-forge -c andynet pheri
pheri ~/miniconda3/envs/test/data/examples/test_phages/phage0000000.fna ./test
