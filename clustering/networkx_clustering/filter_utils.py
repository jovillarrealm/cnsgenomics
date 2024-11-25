import pandas as pd
import os
import params


def extract_code(field: str) -> str | None:
    GC_len = 13
    if field.startswith("GC"):
        code = field[:GC_len]
        return code


def filter_filename(path, filter_str):
    """Filters the filename part of a given path.

    Args:
      path: The input path string.
      filter_str: The string to add to the filename.

    Returns:
      The filtered path string.
    """

    filename, extension = os.path.splitext(path)
    filtered_filename = filename + "_" + filter_str
    return filtered_filename + extension


def apply_filter(csv_path):
    df: pd.DataFrame = pd.read_csv(csv_path, sep=";")
    df = df[
        (df[params.assembly_length].gt(params.max_assembly_length))
        & (df[params.number_of_sequences].lt(params.max_number_of_sequences))
        & (
            (df[params.N50].gt(params.max_N50))
            & (df[params.N_percentage].lt(params.max_N_percentage))
        )
    ]
    new_filename = filter_filename(csv_path, "filtered")
    df.to_csv(new_filename, sep=";", index=False)
    return df, new_filename


def to_dict(df: pd.DataFrame):
    dict_f: dict[str, dict[str, float]] = dict()
    for rec in df.to_records():
        code = extract_code(rec[params.filename])
        dict_f[code] = {
            params.filename: rec[params.filename],
            params.assembly_length: rec[params.assembly_length],
            params.number_of_sequences: rec[params.number_of_sequences],
            params.average_length: rec[params.average_length],
            params.largest_contig: rec[params.largest_contig],
            params.shortest_contig: rec[params.shortest_contig],
            params.N50: rec[params.N50],
            params.N_percentage: rec[params.N_percentage],
        }
    return dict_f

def apply_criteria(candidates: dict) -> dict | None:
    """
    Appies the following criteria:
        stray no further than 10% from the max assembly_length
        get max N50
    """
    if candidates:
        cand_i = candidates.values()
        max_len = max(cand_i, key=lambda x: x[params.assembly_length])[params.assembly_length]
        appropriate_length_assemblies = tuple(
            filter(lambda i: i[params.assembly_length] > max_len * 0.9, cand_i)
        )
        result: dict = max(appropriate_length_assemblies, key=lambda i: i[params.N50])
        return result

if __name__ == "__main__":
    import sys

    stats_file_name = sys.argv[1]
    apply_filter(stats_file_name)
