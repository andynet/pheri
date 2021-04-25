#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 13:37:51 2021

@author: andy
"""

import pandas as pd
# import sklearn
import pickle

# %%
cluster_assignments = "data/010_mcl.clusters"

with open(cluster_assignments, 'r') as f:
    lines = f.readlines()
    
phages = []
genes = []
clusters = []
for i in range(len(lines)):
    lines[i] = lines[i].strip()
    if lines[i].startswith('%') or lines[i] == "":
        continue
    tmp, cluster = lines[i].split('\t')
    phage, gene = tmp.split('_')
    phages.append(phage)
    genes.append(gene)
    clusters.append(cluster)
    
    
    
# %%
matrix_file = "data/012_matrix.mcl.fs.tsv"
matrix = pd.read_csv(matrix_file, sep='\t', index_col=0)


# %%
model_file = "data/013_Acinetobacter.model.mcl.fs.pkl"
model_pkl = open(model_file, 'rb')
mdl = pickle.load(model_pkl)  

