#!/usr/bin/python3

from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import argparse
import pickle
import glob


# %%
def read_cluster_file(f):
    df = pd.read_csv(f, sep='\t', skiprows=(0, 1), header=None, index_col=0)
    df.index = list(df.index)
    df.columns = ["cluster"]
    return df


def create_representation(sample_id, matrix_file, blast_result, prot2clstr_df):
    phage_repr_df = pd.DataFrame(
        data=0, 
        index=[sample_id], 
        columns=pd.read_csv(matrix_file, sep='\t', index_col=(0)).columns
    )
    
    blast = pd.read_csv(blast_result, sep='\t', header=None)
    
    clstr_column_name = prot2clstr_df.columns[0] 
    phage_row_name = phage_repr_df.index[0]
    
    not_used = 0
    for i, row in blast.iterrows():
        hit = row[1]
        cluster = "cluster{:>05}".format(prot2clstr_df.loc[hit, clstr_column_name])
        if cluster in phage_repr_df.columns:
            phage_repr_df.loc[phage_row_name, cluster] += 1
        else:
            not_used += 1
        
    return phage_repr_df


def main():
    parser = argparse.ArgumentParser(description="Predict phage host.")
    parser.add_argument("--blast_file")
    parser.add_argument("--clusters_file")
    parser.add_argument("--matrix_file")    
    args = parser.parse_args()
    
    # args.blast_file = "prokka/test.blast"
    # args.clusters_file = "data/010_mcl.clusters"
    # args.matrix_file = "data/012_matrix.mcl.fs.tsv"
    
    out_vector = args.blast_file[0:-6] + ".vec.tsv"
    out_result = args.blast_file[0:-6] + ".res.tsv"
    sample_id = args.blast_file.split('/')[-1].split('.')[0]
    
    prot2clstr_df = read_cluster_file(args.clusters_file)
    representation_df = create_representation(sample_id, args.matrix_file, args.blast_file, prot2clstr_df)
    models_tsv = glob.glob("data/*.pkl")
    representation_df.to_csv(out_vector, sep='\t')
    
    result_df = pd.DataFrame(columns=["sample_id", "infects", "host", "score"])
    result_df = result_df.astype({"infects": "bool", "score": "float64"})
    
    for model in models_tsv:
        
        model_name = model.split('.')[0].split('_')[-1]
    
        model_pkl = open(model, 'rb')
        mdl = pickle.load(model_pkl)          # type: DecisionTreeClassifier
    
        prediction = mdl.predict(representation_df).squeeze()
        probs = mdl.predict_proba(representation_df).squeeze().round(4)[prediction]
        
        infects = (prediction == 1)
        result_df.loc[len(result_df)] = [sample_id, infects, model_name, probs]
    
    result_df = result_df.sort_values(by=["infects", "score", "host"], ascending=False)
    result_df.to_csv(out_result, sep='\t')


if __name__ == "__main__":
    main()