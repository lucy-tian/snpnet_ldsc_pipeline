#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import sys

sscore_dfs = []
for p in phenotypes:
    base_ukbb_afr = []
    ##baseline
    base_df = pd.read_csv('baselines/406k_geno_v2_UKB_18PCs/fit_w_val/' + sys.argv[1]  + '/' + p + '/snpnet.sscore.txt', sep='\t')
    base_df['trained_cohort'] = ['base'] * len(base_df)
    base_ukbb_afr.append(base_df)
    ##ukbb
    ukbb_df = pd.read_csv('ukbb_0.9_0.01/20230930/406k_geno_v2_UKB_18PCs/fit_w_val/' + sys.argv[1]  + '/' + p + '/snpnet.sscore.txt', sep='\t')
    ukbb_df['trained_cohort'] = ['ukb'] * len(ukbb_df)
    base_ukbb_afr.append(ukbb_df)
    ##afr
    afr_df = pd.read_csv('mvp_afr_0.9_0.01/20230930/406k_geno_v2_UKB_18PCs/fit_w_val/' + sys.argv[1]  + '/' + p + '/snpnet.sscore.txt', sep='\t')
    afr_df['trained_cohort'] = ['afr'] * len(afr_df)
    base_ukbb_afr.append(afr_df)
    merged_df = base_df.iloc[:, [1, -2]].merge(ukbb_df.iloc[:, [1, -2]], on='IID')
    merged_df = merged_df.rename(columns={p + '_SUM_x': p + '_baseline', p + '_SUM_y': p + '_ukbb'})
    new_merge = merged_df.merge(afr_df.iloc[:, [1, -2]], on='IID')
    new_merge = new_merge.rename(columns={p + '_SUM': p + '_afr'})
    
    ##append to back to eval
    sscore_dfs.append(new_merge)


phenotype_data = pd.read_csv('/net/bmc-lab5/data/kellis/group/tanigawa/share/lucytian/20230626/phe.tsv.gz', sep='\t', compression = 'gzip')

phenotypes = pd.read_csv('phenotypes.txt', header = None)[0].tolist()

index = 0
r2r_input = []
for p in phenotypes:
    df = phenotype_data[['#FID', 'IID', p]].merge(sscore_dfs[index], on = 'IID')
    index += 1
    r2r_input.append(df.iloc[:, 2:])
    
r2r_input_nona = [i.dropna() for i in r2r_input]

for i in np.arange(len(phenotypes)):
    r2r_input_nona[i].to_csv('sscore_by_pheno/' + sys.argv[1] + '_' + phenotypes[i] + '_input.tsv', sep = '\t', index=False)
    