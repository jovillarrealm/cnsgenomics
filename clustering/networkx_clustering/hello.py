import networkx as nx
import matplotlib.pyplot as plt
import io
import scipy
import sys
import csv


# Function to create clusters with weighted edges based on threshold
def create_clusters_with_weights(filename, threshold):
    # Create an empty graph
    G = nx.Graph()

    # Open and read the CSV file
    with open(filename, "r") as file:
        reader = csv.DictReader(file, delimiter=";", fieldnames=["G1", "G2", "ANI_HG"])

        # Add weighted edges to the graph if AverageIdentity is above threshold
        for row in reader:
            G1 = row["G1"]
            G2 = row["G2"]
            avg_identity = float(row["ANI_HG"])

            # Add the edge with a weight if the identity is above the threshold
            if avg_identity >= threshold and G1 != G2:
                G.add_edge(G1, G2, weight=avg_identity)
            G.add_node(G1)
            G.add_node(G2)


    # Find connected components, which are your clusters
    clusters = list(frozenset(i) for i in nx.connected_components(G))
    
    # Find isolated nodes (nodes with no edges)
    isolated_nodes = list(frozenset([i]) for i in nx.isolates(G))

    # Find connected nodes (all nodes that have at least one connection)
    connected_nodes = list(set(clusters) - set(isolated_nodes))

    # Extract the edges with weights for each cluster
    weighted_clusters = [
        {
            "nodes": list(cluster),
            "edges": [(u, v, G[u][v]["weight"]) for u, v in G.edges(cluster)],
        }
        for cluster in clusters
        # for cluster in clusters if len(list(cluster)) > 3
    ]

    return G, weighted_clusters, connected_nodes, isolated_nodes



if __name__ == "__main__":
    # csv_file_name = sys.argv[1]
    csv_file_name = "/home/jorge/22julia/cnsgenomics/error_compare/s2400-d131072.out.csv"
    # Load the CSV data into a pandas DataFrame
    # Adjust the 'sep' parameter if your CSV uses a different delimiter
    thresholds = [100.0, 99.9, 99.5, 99.0, 98.0, ]
    for threshold in thresholds:
        print(f"Doing {threshold}")
        with open(f"{threshold}_clusters.csv", "w") as f:
            with open(f"{threshold}_isolates.csv", "w") as g:
                G, w_clusters, clusters, isolates = create_clusters_with_weights(
                    csv_file_name, threshold
                )
                connected_writer = csv.writer(f, delimiter=";")
                clusters = sorted(clusters, key=len, reverse=True)
                for cluster in clusters:
                    connected_writer.writerow(cluster)
                isolates = (tuple(isolate)[0] for isolate in isolates)
                g.write('\n'.join(isolates))
                    
