import sys
import os
import clusters_utils as clusters_utils
import filter_utils as filter_utils
import link_utils
import params


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python script.py <hyper-gen-output-file> <stats-file> <genomic-dir>"
        )
        print("Stats file is filtered again anyway.")
        print("hyper-gen-output may have been filtered before this step")
        print("hyper-gen-output is expected to have been filtered before this step.")
        sys.exit(1)
    tsv_file_name = sys.argv[1]
    stats_file_name = sys.argv[2]
    genomic_dir = sys.argv[3]

    for clusters, isolates, threshold in clusters_utils.write_clusters(tsv_file_name):
        df, filtered_path = filter_utils.apply_filter(stats_file_name)
        dict_f = filter_utils.to_dict(df)

        representatives:list[str] = []

        for cluster in clusters:
            candidates: dict[str] = dict()
            for genome in cluster:
                genome = filter_utils.extract_code(genome)
                if genome in dict_f:
                    candidates[genome] = dict_f[genome]
            chosen_genome = filter_utils.apply_criteria(candidates)
            if chosen_genome:
                chosen_name = filter_utils.extract_code(chosen_genome[params.filename])
                if chosen_name:
                    representatives.append(chosen_name)
        isolates = tuple(filter(lambda i: filter_utils.extract_code(i) in dict_f, isolates))
        representatives.extend(isolates)

        link_utils.make_filter_links(stats_file_name, genomic_dir, threshold)

        filename, _ = os.path.splitext(tsv_file_name)
        filtered_filename = filename + "_" + str(threshold)+ "represent.txt"
        with open(filtered_filename, "w") as g:
            g.write("\n".join(representatives))
