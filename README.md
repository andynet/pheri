# PHERI: phage host exploration through protein clustering and decision trees

## Introduction
PHERI is a tool to predict the phage hosts from the phage sequence in FASTA format. 
Currently, it is able to predict 50 host genera with high accuracy (~97%).
The database of proteins, clustering of proteins and pretrained models were 
obtained from the [preprocessing pipeline](https://github.com/andynet/pheri_preprocessing) and due to the computational complexity
of these steps are included in the tool. 
## Installation
The recommended way to install PHERI is through [conda](https://docs.conda.io/en/latest/) installer. 
PHERI uses 3rd party dependencies, which can be found in the bioconda and conda-forge channel, and installed automatically with the following command:
```bash
conda install -c bioconda -c conda-forge -c andynet pheri
```
## Running PHERI
The input for the PHERI tool should be a single file representing a single phage in the FASTA format.
Furthermore, PHERI requires an output directory, where the results will be stored.
We included the test set as an example. 
To run the example, use these commands:
``` bash
conda create -n test
conda install -c bioconda -c conda-forge -c andynet pheri
pheri ~/miniconda3/envs/test/data/examples/test_phages/phage0000000.fna ./test
```
## Output files
The files with extensions .fna, .faa, .blast, and .vec.tsv are mainly for sanity checks and can be safely deleted.

| extension | description                                                                                                               |
|-----------|---------------------------------------------------------------------------------------------------------------------------|
| .fna      | The original FASTA file copied.                                                                                           |
| .faa      | The genes predicted from FASTA file by Prokka.                                                                            |
| .blast    | The assignments of clusters based on the internal database of genes and their cluster assignments.                        |
| .vec.tsv  | The feature vector used as an input to the classifier.                                                                    |
| .res.tsv  | The main results. The table contains 50 rows for each of the genera currently predicting and the score of the prediction. |
## Results
The PHERI results on the testing dataset (n=1201).

| host              | TP  | FP | FN | TN   |
|-------------------|-----|----|----|------|
| Acinetobacter     | 9   | 4  | 2  | 1186 |
| Aeromonas         | 6   | 2  | 3  | 1190 |
| Arthrobacter      | 46  | 3  | 2  | 1150 |
| Bacillus          | 30  | 11 | 5  | 1155 |
| Brucella          | 6   | 0  | 1  | 1194 |
| Burkholderia      | 5   | 2  | 2  | 1192 |
| Campylobacter     | 11  | 3  | 4  | 1183 |
| Caulobacter       | 2   | 0  | 2  | 1197 |
| Cellulophaga      | 1   | 2  | 6  | 1192 |
| Citrobacter       | 1   | 4  | 4  | 1192 |
| Clostridioides    | 4   | 0  | 1  | 1196 |
| Clostridium       | 2   | 2  | 3  | 1194 |
| Corynebacterium   | 3   | 0  | 1  | 1197 |
| Cronobacter       | 2   | 7  | 3  | 1189 |
| Cutibacterium     | 25  | 0  | 0  | 1176 |
| Enterococcus      | 6   | 4  | 4  | 1187 |
| Erwinia           | 4   | 0  | 5  | 1192 |
| Escherichia       | 94  | 21 | 33 | 1053 |
| Flavobacterium    | 6   | 4  | 1  | 1190 |
| Gordonia          | 59  | 2  | 3  | 1137 |
| Helicobacter      | 6   | 1  | 0  | 1194 |
| Klebsiella        | 5   | 7  | 13 | 1176 |
| Lactobacillus     | 7   | 5  | 4  | 1185 |
| Lactococcus       | 43  | 4  | 5  | 1149 |
| Leuconostoc       | 4   | 0  | 0  | 1197 |
| Listeria          | 5   | 2  | 2  | 1192 |
| Mannheimia        | 2   | 1  | 1  | 1197 |
| Microbacterium    | 22  | 2  | 1  | 1176 |
| Moraxella         | 7   | 1  | 0  | 1193 |
| Mycobacterium     | 0   | 2  | 1  | 1198 |
| Mycolicibacterium | 321 | 4  | 1  | 875  |
| Paenibacillus     | 5   | 0  | 1  | 1195 |
| Pectobacterium    | 1   | 2  | 5  | 1193 |
| Proteus           | 2   | 2  | 1  | 1196 |
| Pseudoalteromonas | 4   | 4  | 2  | 1191 |
| Pseudomonas       | 45  | 8  | 12 | 1136 |
| Ralstonia         | 1   | 1  | 6  | 1193 |
| Rhizobium         | 1   | 0  | 2  | 1198 |
| Rhodococcus       | 11  | 1  | 1  | 1188 |
| Ruegeria          | 3   | 5  | 0  | 1193 |
| Salmonella        | 22  | 7  | 20 | 1152 |
| Shigella          | 3   | 6  | 8  | 1184 |
| Staphylococcus    | 36  | 5  | 3  | 1157 |
| Stenotrophomonas  | 0   | 0  | 3  | 1198 |
| Streptococcus     | 39  | 9  | 1  | 1152 |
| Streptomyces      | 27  | 3  | 8  | 1163 |
| Synechococcus     | 29  | 3  | 0  | 1169 |
| Vibrio            | 18  | 3  | 14 | 1166 |
| Xanthomonas       | 2   | 3  | 3  | 1193 |
| Yersinia          | 2   | 5  | 3  | 1191 |

## Dependencies
The dependencies are automatically installed with the conda installer. 
This list can help you, when installing from source (not recommended).

- python >=3.6
- prokka >=1.14
- blast
- scikit-learn =0.18.0
- scipy <0.19
- pandas

## Citation
If you use our tool, please cite:
```
Baláž, Andrej, et al.
PHERI-Phage Host Exploration pipeline.
bioRxiv (2020).
```
