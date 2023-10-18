#!/bin/bash
#SBATCH -o %j.out 
#SBATCH -e %j.err

set -beEuo pipefail


data_d='/home/lucytian/data/1_Single_Cell_PRS/2_cV2F'
mvp_afr_d=${data_d}/mvp_afr_0.9_0.01/20230930
ukbb_d=${data_d}/ukbb_0.9_0.01/20230930
param_value=$1


##STEP 0: Evaluate model performance difference is significant via R2REDUX
bash 0a_zstd.sh ${mvp_afr_d}
bash 0a_zstd.sh ${ukbb_d}

python 0b_r2rdux_input.py param_${param_value}

conda activate snpnet

Rscript 0c_r2redux.R ${param_value}

conda deactivate

##Penalty Param will not be a variable in the following steps

##STEP 1: Run ldsc and h2
python 1a_make_annot.py ${mvp_afr_d}/mvp_afr_0.9_0.01_baseline_annotation_full.cv2f.txt ${ukbb_d}/ukbb_0.9_0.01_baseline_annotation_full.cv2f.txt

conda activate ldsc

bash 1b_run_ldsc.sh
bash 1c_run_h2.sh

##STEP 2: Calculate Tau*

conda deactivate
python 2a_make_annot_tau.py