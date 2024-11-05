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
    return os.path.join(os.path.dirname(path), filtered_filename + extension)


def apply_filter(csv_path):
    df: pd.DataFrame = pd.read_csv(csv_path, sep=";")
    df = df[
        (assembly_length > 4_000_000)
        and (number_of_sequences > 1880)
        and (N50 > 50_000)
        and (N_percentage < 0.87)
    ]
    print(df.head())
    new_filename = filter_filename(csv_path)
    df.to_csv(new_filename, sep=";")
    return df


def to_dict(df: pd.DataFrame):
    dict_f = dict()
    for rec in df.to_records():
        code = extract_code(rec[filename])
        dict_f[code] = {
            assembly_length: rec[assembly_length],
            number_of_sequences: rec[number_of_sequences],
            average_length: rec[average_length],
            largest_contig: rec[largest_contig],
            shortest_contig: rec[shortest_contig],
            N50: rec[N50],
            N_percentage: rec[N_percentage],
        }
    return dict_f
