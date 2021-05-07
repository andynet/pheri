#!/bin/bash

fasta=${1}
outdir='result'

tmp=${fasta%.*}
sample_name=${tmp##*/}

echo ${sample_name}

mkdir -p ${outdir}

echo "Predicting genes with prokka."
prokka                                      \
    --outdir ${outdir}                      \
    --force                                 \
    --prefix ${sample_name}                 \
    --locustag 'protein'                    \
    --kingdom Viruses                       \
    --cpus 0                                \
    --noanno                                \
    --norrna                                \
    --notrna                                \
    ${fasta}                                \
    1> ${outdir}/${sample_name}.log.out     \
    2> ${outdir}/${sample_name}.log.err

# create index with:
# makeblastdb -in 008_train.cd-hit.genes.faa -dbtype prot

echo "Finding clusters"
blastp                                              \
    -query ${outdir}/${sample_name}.faa             \
    -db "data/blastdb/train_genes.faa"              \
    -out ${outdir}/${sample_name}.blast             \
    -outfmt "6 qseqid sseqid score pident evalue"   \
    -max_hsps 1	                                    \
    -max_target_seqs 1
    
echo "Predicting host"
python ./main.py    \
    --blast_file ${outdir}/${sample_name}.blast \
    --clusters_file data/clusters.tsv  	        \
    --matrix_file data/features.tsv

extensions=(err ffn fsa gbk gff log log.err log.out sqn tbl tsv txt);
for ext in ${extensions[@]}; do
    rm ${outdir}/${sample_name}.${ext}
done;

