import pandas as pd
import numpy as np

# organelle = "Mitochondria"

# Read the RNA single cell type data into a pandas dataframe and pivot it
df_rna_sca = pd.read_csv('data/rna_single_cell_type.tsv', sep="\t")
df_rna_sca_wide = pd.pivot(df_rna_sca, index=['Gene','Gene name'], columns = 'Cell type', values = 'nTPM')

# Reset the index and drop the first column
df_rna_sca_wide.reset_index(inplace=True)
df_rna_sca_wide.reset_index(drop=True)
df_rna_sca_wide = df_rna_sca_wide.iloc[:,1:]

# Rename the first column and set the index
df_rna_sca_wide.rename(columns={'Gene name':'GENENAME'}, inplace=True)
df_rna_sca_wide.set_index(['GENENAME'], inplace=True)

# Read the gene location data into a pandas dataframe and clean it
# df_location_initial = pd.read_csv("./data/subcellular_location.tsv", sep="\t")
df_location_initial = pd.read_csv("data/subcellular_location.tsv", sep="\t")
df_location = df_location_initial.iloc[:, :4]
df_location = df_location.drop(df_location.columns[[0, 2]], axis=1)
df_location = df_location.dropna(how='any')

# Rename the column and get the list of gene names
df_location.rename(columns={'Gene name':'Gene'}, inplace=True)
org_gene_names = df_location['Gene'].tolist()

# Filter the RNA single cell type data by organelle if specified
df_org_rna_sca_wide = df_rna_sca_wide
# if organelle != "None":
#     df_org_location = df_location.loc[df_location['Main location'].str.contains(organelle)]
#     org_gene_names = df_org_location['Gene'].tolist()
#     df_org_rna_sca_wide = df_rna_sca_wide[df_rna_sca_wide.index.isin(org_gene_names)]    

# Return the log of the RNA single cell type data
df = np.log1p(df_org_rna_sca_wide)

# nameconversion = pd.read_csv("data/nameconversion.csv")

mt_list = df_location.loc[df_location['Main location'].str.contains("Mitochondria")]['Gene'].to_list()
er_list = df_location.loc[df_location['Main location'].str.contains("Endoplasmic reticulum")]['Gene'].to_list()
ga_list = df_location.loc[df_location['Main location'].str.contains("Golgi apparatus")]['Gene'].to_list()