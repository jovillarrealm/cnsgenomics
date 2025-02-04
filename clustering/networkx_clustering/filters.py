import os
import polars as pl
import params

def extract_code(field: str) -> str | None:
    GC_len = 13
    if field.startswith("GC"):
        code = field[:GC_len]
        return code

def filter_filename(path, filter_str):
    filename, extension = os.path.splitext(path)
    filtered_filename = filename + "_" + filter_str
    return filtered_filename + extension

def apply_filter(csv_path):
    df = pl.read_csv(csv_path, separator=";")

    df = df.filter(
        (pl.col(params.assembly_length) > params.max_assembly_length)
        & (pl.col(params.number_of_sequences) < params.min_number_of_sequences)
        & (pl.col(params.N50) > params.max_N50)
        & (pl.col(params.N_percentage) < params.min_N_percentage)
    )

    new_filename = filter_filename(csv_path, "filtered")
    df.write_csv(new_filename, separator=";")
    return df, new_filename

def to_dict(df: pl.DataFrame):
    dict_f: dict[str, dict[str, float]] = {}
    for row in df.iter_rows():  # Iterate through rows
        code = extract_code(row[df.columns.index(params.filename)])
        if code is not None:
            dict_f[code] = {
                params.filename: row[df.columns.index(params.filename)],
                params.assembly_length: row[df.columns.index(params.assembly_length)],
                params.number_of_sequences: row[df.columns.index(params.number_of_sequences)],
                params.average_length: row[df.columns.index(params.average_length)],
                params.largest_contig: row[df.columns.index(params.largest_contig)],
                params.shortest_contig: row[df.columns.index(params.shortest_contig)],
                params.N50: row[df.columns.index(params.N50)],
                params.N_percentage: row[df.columns.index(params.N_percentage)],
            }
    return dict_f


def apply_criteria(candidates: dict, preferred_set: set | None) -> dict | None:
    if candidates:
        cand_i = list(candidates.values()) # Convert to list for easier manipulation
        if preferred_set:
            filtered_cand = list(filter(lambda i: extract_code(i[params.filename]) in preferred_set, cand_i))
            if filtered_cand:
                if len(filtered_cand) == 1:
                    return filtered_cand[0]  # Return the single element directly
                elif len(filtered_cand) > 1:
                    cand_i = filtered_cand

        if not cand_i: # Handle the case where filtered_cand is empty after the filter
            return None

        max_len = max(cand_i, key=lambda x: x[params.assembly_length])[params.assembly_length]
        appropriate_length_assemblies = tuple(
            filter(lambda i: i[params.assembly_length] > max_len * 0.9, cand_i)
        )
        if appropriate_length_assemblies: # Check if appropriate_length_assemblies is not empty
            result: dict = max(appropriate_length_assemblies, key=lambda i: i[params.N50])
            return result
        else:
            return None # Return None if no appropriate assemblies are found
    return None # Return None if the initial candidates dictionary is empty


if __name__ == "__main__":
    import sys
    _, stats_file_name = sys.argv
    apply_filter(stats_file_name) # No need to pass preferred_list here as it is not used in apply_filter.