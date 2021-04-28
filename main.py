#!/usr/bin/python3

from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import argparse
import pickle
import glob


# %% inputs
blast_result = "prokka/test.blast"
clusters = "data/010_mcl.clusters"
matrix_file = "data/012_matrix.mcl.fs.tsv"

# %% outputs
out_vector = "prokka/test.vector.out"
out_result = "prokka/test.result"

# %%
clstr = pd.read_csv(clusters, sep='\t', skiprows=(0, 1), header=None, index_col=0)
clstr.index = list(clstr.index)
clstr.columns = ["cluster_num"]

columns = pd.read_csv(matrix_file, sep='\t', index_col=(0)).columns

# %%
new_record = pd.DataFrame(0, index=["test"], columns=columns)
not_used = 0

# %%
with open(blast_result) as f:
    lines = f.readlines()
    
for line in lines:
    hit = line.strip().split()[1]
    cluster = clstr.loc[hit, "cluster_num"]
    cluster = f"cluster{cluster:>05}"
    if cluster in new_record.columns:
        new_record.loc["test", cluster] += 1
    else:
        not_used += 1
    
# %%
blast = pd.read_csv(blast_result, sep='\t', header=None)

for i, row in blast.iterrows():
    hit = row[1]
    cluster = clstr.loc[hit, "cluster_num"]
    cluster = f"cluster{cluster:>05}"
    if cluster in new_record.columns:
        new_record.loc["test", cluster] += 1
    else:
        not_used += 1

# %%
models_tsv = glob.glob("data/*.pkl")
new_record.to_csv(out_vector, sep='\t')

for model in models_tsv:

    model_pkl = open(model, 'rb')
    mdl = pickle.load(model_pkl)          # type: DecisionTreeClassifier

    prediction = mdl.predict(new_record)

    with open(out_result, 'a') as f:
        f.write('{}\t{}\t{}\n'.format(blast_result, model, prediction))
