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
    
makeblastdb -in 008_train.cd-hit.genes.faa -dbtype prot

blastp                                              \
    -query prokka/test.faa                          \
    -db data/008_train.cd-hit.genes.faa             \
    -out prokka/test.blast                          \
    -outfmt "6 qseqid sseqid score pident evalue"   \
    -max_target_seqs 1
