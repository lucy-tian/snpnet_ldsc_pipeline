#!/bin/bash

bfile_dir="1000G_EUR_Phase3_cV2F"
#annot_dir="/home/lucytian/data/1_Single_Cell_PRS/ldsc_cCRE/1000G_EUR_geno/ldscores"
annot_dir="ldscore"
out_dir="ldscore"
#snp_list_dir="/net/bmc-lab5/data/kellis/group/tanigawa/data/alkesgroup/LDSCORE/baseline_v1.2"

python /home/lucytian/data/0_SOFTWARE/ldsc/ldsc.py --l2 --bfile ${bfile_dir}/1000G.EUR.QC.${1} --ld-wind-cm 1 --annot ${annot_dir}/1000G_EUR_geno.${1}.annot.gz --out ${out_dir}/1000G_EUR_geno.${1}