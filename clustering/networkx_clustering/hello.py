import sys
import os
import clusters_utils as clusters_utils
import filter_utils as filter_utils


def apply_criteria(candidates: dict):
    """
    Appies the following criteria:
        stray no further than 10% from the max assembly_length
        get max N50
    """
    if candidates:
        cand_i = candidates.values()
        max_len = max(cand_i, key=lambda x: x["assembly_length"])["assembly_length"]
        appropriate_length_assemblies = tuple(
            filter(lambda i: i["assembly_length"] > max_len * 0.9, cand_i)
        )
        result = max(appropriate_length_assemblies, key=lambda i: i["N50"])
        return result


if __name__ == "__main__":
    csv_file_name = sys.argv[1]
    stats_file_name = sys.argv[2]

    clusters, isolates = clusters_utils.write_clusters(csv_file_name)
    df = filter_utils.apply_filter(stats_file_name)
    dict_f = filter_utils.to_dict(df)
    representatives = []

    for cluster in clusters:
        candidates: dict[str] = dict()
        for genome in cluster:
            genome = filter_utils.extract_code(genome)
            if genome in dict_f:
                candidates[genome] = dict_f[genome]
        chosen_genome = apply_criteria(candidates)
        if chosen_genome:
            representatives.append(chosen_genome[filter_utils.filename])
    r_len = len(representatives)
    representatives.extend(isolates)
    filename, _ = os.path.splitext(csv_file_name)
    filtered_filename = filename + "_" + "represent.txt"
    with open(filtered_filename, "w") as g:
        g.write("\n".join(representatives))
