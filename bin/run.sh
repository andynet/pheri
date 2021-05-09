#!/bin/bash

if [[ ${#} -ne 1 ]]; then
    echo "Usage: ${0} <fasta>";
    exit 0;
fi

fasta=${1}
outdir=$(dirname ${fasta})
base=$(basename ${fasta})
sample_name=${base%.*}

echo -e "outdir = ${outdir} \nsample_name = ${sample_name} "

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
if [[ ! -s ${outdir}/${sample_name}.faa ]]; then
    echo "No genes were found by prokka. Exiting...";
    exit 0;
fi


echo "Finding clusters"
blastp                                              \
    -query ${outdir}/${sample_name}.faa             \
    -db "data/blastdb/train_genes.faa"              \
    -out ${outdir}/${sample_name}.blast             \
    -outfmt "6 qseqid sseqid score pident evalue"   \
    -max_hsps 1	                                    \
    -max_target_seqs 1
    
echo "Predicting host"
python main.py    \
    --blast_file ${outdir}/${sample_name}.blast \
    --clusters_file data/clusters.tsv  	        \
    --matrix_file data/features.tsv

extensions=(err ffn fsa gbk gff log log.err log.out sqn tbl tsv txt);
for ext in ${extensions[@]}; do
    rm ${outdir}/${sample_name}.${ext}
done;

echo "Finished successfully. Results are stored in ${outdir}/${sample_name}.res.tsv. \n"

