import sys
import clusters_utils as clusters_utils
import filter_utils as filter_utils


if __name__ == "__main__":
    # csv_file_name = sys.argv[1]
    # stats_file_name = sys.argv[2]
    csv_file_name = (
        "/home/jorge/22julia/cnsgenomics/error_compare/s2400-d131072.out.csv"
    )
    stats_file_name = "/home/jorge/22julia/Streptomyces_16-10-2024_stats.csv"

    clusteres, isolates = clusters_utils.write_clusters(csv_file_name)
    df = filter_utils.apply_filter(stats_file_name)
    dict_f = filter_utils.to_dict(df)
    results = []

    for cluster in clusteres:
        candidates = dict()
        for genome in cluster:
            if genome in dict_f:
                candidates[genome] = dict_f[genome]
        candidates = list(candidates.items())
        sorted(candidates, key=criteria)

def criteria(a,b):
    # stray no further than 10% from max assembly_length
    # get max N50
    # number of sequences somthing something
    pass