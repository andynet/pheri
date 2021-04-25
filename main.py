#!/usr/bin/python3

from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
import subprocess
import argparse
import pickle
import os


def create_dict(m):
    genes_to_cluster = dict()
    with open(m) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        members = line.strip().split('\t')
        for member in members:
            genes_to_cluster[member] = i

    return genes_to_cluster


def calculate_vector(blast, genes_to_cluster):
    vector = []
    with open(blast) as f:
        lines = f.readlines()

    for line in lines:
        target_gene = line.split()[1]
        vector.append(genes_to_cluster[target_gene])

    vector = list(set(vector))
    vector.sort()

    return vector


# %%
parser = argparse.ArgumentParser(description='Predict host from phage fasta.')
parser.add_argument('-i', '--fasta', required=True)
parser.add_argument('-o', '--out_dir', required=True)
args = parser.parse_args()

# %%
fasta_name = os.path.basename(args.fasta)

prokka_command = '/root/prokka/bin/prokka ' \
                 '--kingdom Viruses '       \
                 '--force '                 \
                 '--outdir {} '             \
                 '--prefix {} '             \
                 '{}'.format(args.out_dir, fasta_name, args.fasta)

subprocess.run(prokka_command, shell=True)
print(prokka_command)

blastp_command = 'blastp '                                        \
                 '-query {}/{}.faa '                                     \
                 '-db {} '                                        \
                 '-out {}/{}.blast '                                 \
                 '-outfmt "6 qseqid sseqid score pident evalue" ' \
                 '-max_target_seqs 1'.format(args.out_dir, fasta_name, '/app/files/007_train.cd-hit.genes.fasta',
                                             args.out_dir, fasta_name)

subprocess.run(blastp_command, shell=True)
print(blastp_command)

genes_blast = '{}/{}.blast'.format(args.out_dir, fasta_name)
cluster_tsv = '/app/files/010_mcl.tsv'
matrix_tsv = '/app/files/011_matrix.mcl.fs.tsv'
models_tsv = [
              '/app/files/013_model.mcl.fs.arthrob.pkl', '/app/files/013_model.mcl.fs.lactoco.pkl',
              '/app/files/013_model.mcl.fs.staphyl.pkl', '/app/files/013_model.mcl.fs.escheri.pkl',
              '/app/files/013_model.mcl.fs.mycobac.pkl', '/app/files/013_model.mcl.fs.strepto.pkl',
              '/app/files/013_model.mcl.fs.gordoni.pkl', '/app/files/013_model.mcl.fs.pseudom.pkl'
              ]
out_vector = '{}/{}.vector'.format(args.out_dir, fasta_name)

genes_cluster = create_dict(cluster_tsv)
vctr = calculate_vector(genes_blast, genes_cluster)

# load matrix and create new record for phage
matrix = pd.read_csv(matrix_tsv, sep='\t', header=0, index_col=0)
new_record = pd.DataFrame(np.zeros((1, matrix.shape[1]), dtype=int), columns=matrix.columns, index=[fasta_name])

for item in vctr:
    if 'Cluster_{}'.format(item) in new_record.columns:
        new_record.set_value(fasta_name, 'Cluster_{}'.format(item), 1)
    else:
        print('Cluster_{} is not in the matrix.'.format(item))

new_record.to_csv(out_vector, sep='\t')

for model in models_tsv:

    model_pkl = open(model, 'rb')
    mdl = pickle.load(model_pkl)          # type: DecisionTreeClassifier

    prediction = mdl.predict(new_record)
    spec = os.path.basename(os.path.abspath(model)).split('.')[-2]

    out_result = '{}/{}.{}.result'.format(args.out_dir, fasta_name, spec)

    with open(out_result, 'w') as f:
        f.write('{}\t{}\t{}\n'.format(fasta_name, spec, prediction))
