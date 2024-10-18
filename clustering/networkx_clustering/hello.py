import networkx as nx
import matplotlib.pyplot as plt
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

    # Find connected components, which are your clusters
    clusters = list(nx.connected_components(G))

    # Extract the edges with weights for each cluster
    weighted_clusters = [
        {
            "nodes": list(cluster),
            "edges": [(u, v, G[u][v]["weight"]) for u, v in G.edges(cluster)],
        }
        for cluster in clusters
        # for cluster in clusters if len(list(cluster)) > 3
    ]

    return G, weighted_clusters, clusters


# Function to visualize the graph
def visualize_clusters(G, clusters):
    # Set up the plot
    plt.figure(figsize=(12, 8))

    # Create a layout for the graph
    pos = nx.spring_layout(G, seed=42)  # Spring layout for better visualization

    clusters = filter(lambda cluster: len(cluster["nodes"]) > 3, clusters)
    clusters = [max(clusters,key=lambda cluster: len(cluster["nodes"]))]

    # Draw nodes and edges
    for cluster in clusters:
        subgraph = G.subgraph(cluster["nodes"])

        # Draw nodes (using a unique color per cluster)
        nx.draw_networkx_nodes(subgraph, pos, node_size=300, alpha=0.7)

        # Draw edges with varying widths based on weights
        edges, weights = zip(*nx.get_edge_attributes(subgraph, "weight").items())
        nx.draw_networkx_edges(
            subgraph, pos, edgelist=edges, width=[w / 10 for w in weights], alpha=0.5
        )

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Add a title and show the plot
    plt.title("Clusters of Genomes with Weighted Edges by Average Identity")
    plt.axis("off")
    plt.savefig(f"{threshold}_clusters.png")
    plt.clf()


if __name__ == "__main__":
    # csv_file_name = sys.argv[1]
    csv_file_name = "/home/jorge/22julia/cnsgenomics/error_compare/s2400-d65536.out.csv"
    # Load the CSV data into a pandas DataFrame
    # Adjust the 'sep' parameter if your CSV uses a different delimiter
    thresholds = (i / 10 for i in range(1000, 993, -1))
    for threshold in thresholds:
        print(f"Doing {threshold}")
        with open(f"{threshold}_clusters.csv", "w") as f:
            G, w_clusters, clusters = create_clusters_with_weights(
                csv_file_name, threshold
            )
            visualize_clusters(G, w_clusters)
            paperback_writer = csv.writer(f, delimiter=";")
            clusters = sorted(clusters, key=len, reverse=True)
            for cluster in clusters:
                paperback_writer.writerow(cluster)
