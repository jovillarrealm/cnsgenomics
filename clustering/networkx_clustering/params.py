"""

The clustering problem seems to depend on too many variables at the same time, and they can seem arbitrary.

They were also meant for a single taxon, so they must change several thing on different places accordingly


"""

# For clustering
thresholds = [99.0, 98.0, 97.0, 96.0, 95.0, 94.0, 93.0, 92.0, 91.0, 90.0]

# For filtering
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

max_assembly_length = 4_000_000
min_number_of_sequences = 1_880
max_N50 = 50_000
min_N_percentage = 0.87

# For linking
reference_dir_name = "GENOMIC1_r"
