import pandas as pd
import os

filename = "filename"
assembly_length = "assembly_length"
number_of_sequences = "number_of_sequences"
average_length = "average_length"
largest_contig = "largest_contig"
shortest_contig = "shortest_contig"
N50 = "N50"
GC_percentage = "GC_percentage"
total_N = "total_N"
N_percentage = "N_percentage"


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
    print(df.dtypes)
    print(df.head())
    df = df[
        (df["assembly_length"].gt(4_000_000))
        & (df["number_of_sequences"].lt(1880))
        & ((df["N50"].gt(50_000)) & (df["N_percentage"].lt(0.87)))
    ]
    new_filename = filter_filename(csv_path, "filtered")
    print(new_filename)
    df.to_csv(new_filename, sep=";", index=False)
    return df

def to_dict(df: pd.DataFrame):
    dict_f: dict[str,dict[str,float]] = dict()
    for rec in df.to_records():
        code = extract_code(rec[filename])
        dict_f[code] = {
            filename: rec[filename],
            assembly_length: rec[assembly_length],
            number_of_sequences: rec[number_of_sequences],
            average_length: rec[average_length],
            largest_contig: rec[largest_contig],
            shortest_contig: rec[shortest_contig],
            N50: rec[N50],
            N_percentage: rec[N_percentage],
        }
    return dict_f

if __name__ == "__main__":
    import sys
    stats_file_name = sys.argv[1]
    apply_filter(stats_file_name)