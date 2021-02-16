import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import randomcolor


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


# mengatur size dan warna dari node

rand_color = randomcolor.RandomColor()

person_sizes_dict = data[["person"]].groupby(
    "person", sort=False).size().to_dict()

birthplace_colors_dict = data[["birthplace"]].groupby(
    "birthplace").apply(lambda x: rand_color.generate()[0]).to_dict()


person_birthplace_list = list(data[["person", "birthplace"]].drop_duplicates().to_dict(
    "index").values())

person_colors_dict = {}

for val in person_birthplace_list:
    person_colors_dict[val['person']
                       ] = birthplace_colors_dict[val['birthplace']]


node_sizes = [person_sizes_dict[node]*300 for node in G]
node_colors = [person_colors_dict[node] for node in G]

# membuat gambar network graph dan menyimpannya ke file graph.png
plt.figure(figsize=(25, 25))

options = {
    'edge_color': '#FFDEA2',
    'width': 1,
    'with_labels': True,
    'font_weight': 'regular',
    'font_size': 9
}
plt.title("Oscars Nominees Network Graph by Birthplace")

nx.draw(G, node_size=node_sizes, node_color=node_colors, pos=nx.spring_layout(
    G, k=1),  **options)

plt.savefig("graph.png")
