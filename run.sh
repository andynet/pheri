#!/bin/sh

fasta='data/test.fna'
outdir='prokka'
sample_name='test'

mkdir -p ${outdir}
    
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

blastp                                              \
    -query ${outdir}/${sample_name}.faa             \
    -db data/008_train.cd-hit.genes.faa             \
    -out ${outdir}/${sample_name}.blast             \
    -outfmt "6 qseqid sseqid score pident evalue"   \
    -max_hsps 1	                                    \
    -max_target_seqs 1
    
python ./main.py    \
    --blast_file ${outdir}/${sample_name}.blast \
    --clusters_file data/010_mcl.clusters  	\
    --matrix_file data/012_matrix.mcl.fs.tsv

