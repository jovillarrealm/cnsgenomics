import os
import sys
import params


def create_hardlinks(stats_file, genomic_dir, threshold):
    # Ensure the paths are absolute
    out_dir = os.path.realpath(genomic_dir)
    output_dir = os.path.join(out_dir, params.reference_dir_name + str(threshold))

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the stats file, skipping the first line, and process each line
    with open(stats_file, "r") as f:
        # Skip the header (first line)
        lines = f.readlines()[1:]

        # Process each line
        for line in lines:
            # Extract the first field (before the first ';')
            parts = line.split(";")
            code = parts[0].strip()

            # Create the symbolic link
            src = os.path.join(out_dir, "GENOMIC1", code)
            dest = os.path.join(output_dir, code)

            # Check if the source file exists
            if os.path.exists(src):
                os.link(src, dest)
            else:
                print(f"Source file does not exist: {src}")


def make_filter_links(stats_file, genomic_dir, threshold):
    # Validate the existence of the stats file and genomic directory
    if not os.path.isfile(stats_file):
        print(f"Error: Stats file '{stats_file}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(genomic_dir):
        print(f"Error: Genomic directory '{genomic_dir}' does not exist.")
        sys.exit(1)

    # Create symlinks
    create_hardlinks(stats_file, genomic_dir, threshold)


def make_representative_links(representative_file, genomic_dir, threshold):
    # Validate the existence of the stats file and genomic directory
    if not os.path.isfile(representative_file):
        print(f"Error: Stats file '{representative_file}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(genomic_dir):
        print(f"Error: Genomic directory '{genomic_dir}' does not exist.")
        sys.exit(1)

    # Create links
    create_hardlinks(representative_file, genomic_dir, threshold)

    out_dir = os.path.realpath(genomic_dir)
    output_dir = os.path.join(out_dir, params.reference_dir_name + str(threshold))

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the stats file, skipping the first line, and process each line
    with open(representative_file, "r") as f:
        # Skip the header (first line)
        lines = f.readlines()

        # Process each line
        for line in lines:
            filename = line.strip()

            # Create the symbolic link
            src = os.path.join(out_dir, "GENOMIC1", filename)
            dest = os.path.join(output_dir, filename)

            # Check if the source file exists
            if os.path.exists(src) and not os.path.exists(dest):
                os.link(src, dest)
            else:
                print(f"Source file does not exist: {src}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <stats_file> <genomic_dir>")
        sys.exit(1)
    stats_file = sys.argv[1]
    genomic_dir = sys.argv[2]
    for threshold in params.thresholds:
        make_filter_links(stats_file, genomic_dir, threshold)
