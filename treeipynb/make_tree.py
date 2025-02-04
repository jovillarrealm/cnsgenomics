import kssdtree
import sys

genomic_dir = sys.argv[1]
genomic_dir=genomic_dir.rstrip("/")

threshold = "99"


shuf_file = "L3K10"
sketch_dir = genomic_dir +"_kssd_sketch"
phylip_file = "t" + threshold + ".phy"
newick_file = "t_" + threshold + ".nwk"

conf = {
    "dnj_flag": 1,
    "dnj_method": "dnj",
}


kssdtree.shuffle(k=10, l=3, s=6, o=shuf_file)
#kssdtree.sketch(shuf_file=shuf_file, genome_files=genomic_dir, output=sketch_dir)
#kssdtree.dist(genome_sketch=sketch_dir, output=phylip_file, flag=conf["dnj_flag"])
#kssdtree.build(phylip=phylip_file, output=newick_file, method=conf["dnj_method"])
#kssdtree.visualize(newick=newick_file,  mode="r")
kssdtree.quick(shuf_file=shuf_file+".shuf",genome_files=genomic_dir,output=newick_file,method="dnj", mode="r")

