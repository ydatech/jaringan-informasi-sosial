import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# membaca file csv ./Oscars-demographics-DFE.csv dengan pandas
oscars_data = pd.read_csv("./Oscars-demographics-DFE.csv")

# transformasi data dari Dataframe pandas
data = oscars_data[["person", "birthplace"]]

merged_data = data.merge(data[["person", "birthplace"]].rename(
    columns={"person": "person_target"}), on="birthplace")

clean_data = merged_data[~(merged_data["person"] ==
                           merged_data["person_target"])].drop_duplicates()
clean_data.drop(
    clean_data.loc[clean_data["person_target"] < clean_data["person"]].index.tolist(), inplace=True)


# membuat networkx Grapah dari pandas edgelist
G = nx.from_pandas_edgelist(
    df=clean_data, source="person", target="person_target", edge_attr="birthplace")


# membuat degree distribution
degrees = {}
for n in G.nodes():
    degree = G.degree(n)
    if degree not in degrees:
        degrees[degree] = 0
    degrees[degree] += 1

items = sorted(degrees.items())

# memplot degree distribution
plt.figure()
plt.plot([k for (k, v) in items], [v for (k, v) in items])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title("Oscars Nominees Degree Distribution")
# simpan hasil plot di file
plt.savefig("degree-distribution.png")
