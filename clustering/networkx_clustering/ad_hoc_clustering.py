import sys
import os
import clusters
import filters
import links
import params
import polars as pl


if __name__ == "__main__":
    if len(sys.argv) <= 4:
        print(
            "Usage: python script.py <hyper-gen-output-file> <stats-file> <genomic-dir> <preferred-list>"
        )
        print("Stats file is filtered again anyway.")
        print("hyper-gen-output may have been filtered before this step")
        print("hyper-gen-output is expected to have been filtered before this step.")
        sys.exit(1)
    hyper_gen_tsv_path: str = sys.argv[1]
    stats_file_name: str = sys.argv[2]
    genomic_dir: str = sys.argv[3]
    if len(sys.argv) == 4:
        preferred_list = None
    else:
        preferred_list = sys.argv[4]
    df, filtered_path = filters.apply_filter(stats_file_name)
    dict_f = filters.to_dict(df)
    if dict_f is None:
        raise Exception
    if preferred_list:
        preferred_set = set(pl.read_csv(preferred_list, separator=",")["GCA"])
    for clusters, isolates, threshold in clusters.write_clusters(hyper_gen_tsv_path):
        representatives: list[str] = []

        for cluster in clusters:
            candidates: dict[str, dict] = dict()
            for genome in cluster:
                genome = filters.extract_code(genome)
                if genome is not None:
                    if genome in dict_f:
                        candidates[genome] = dict_f[genome]
            chosen_genomes = filters.apply_criteria(candidates)
            if chosen_genomes:
                for chosen_genome in chosen_genomes:
                    chosen_name = chosen_genome[params.filename]
                    if chosen_name:
                        representatives.append(chosen_name)
        isolates = tuple(
            filter(
                lambda i: filters.extract_code(i) is not None
                and filters.extract_code(i) in dict_f,
                isolates,
            )
        )
        representatives.extend(isolates)
        if preferred_list:
            representatives=list(set(representatives).union(preferred_set))

        filename, _ = os.path.splitext(hyper_gen_tsv_path)
        representative_filename = filename + "_" + str(threshold) + "represent.txt"
        with open(representative_filename, "w") as g:
            g.write("\n".join(representatives))
        links.make_representative_links(
            representative_filename, genomic_dir, threshold
        )

        
