#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sys


# In[10]:


afr_df = pd.read_csv(sys.argv[1], sep = '\t', low_memory=False)


# In[29]:


ukb_df = pd.read_csv(sys.argv[2], sep = '\t', low_memory=False)


# In[40]:


for i in np.arange(1, 23):
    bim = pd.read_csv('~/data/1_Single_Cell_PRS/2_cV2F/ldsc_cV2F/1000G_EUR_Phase3_plink/1000G.EUR.QC.' + str(i) + '.bim', sep='\t', header = None)
    bim.columns = (['CHR', 'SNP', 'CM', 'BP', 'ALT', 'REF'])
    merged_df = afr_df.merge(bim, on = 'SNP')
    merged_df = merged_df.rename(columns={'cV2F': 'cV2F_afr'})
    merged_df = merged_df.merge(ukb_df, on = 'SNP')
    merged_df = merged_df.rename(columns={'cV2F': 'cV2F_ukbb'})
    merged_df[['CHR', 'BP', 'SNP', 'CM', 'cV2F_afr', 'cV2F_ukbb']].to_csv('ldscore/1000G_EUR_geno.' + str(i) + '.annot.gz', compression = 'gzip', sep = '\t', index=False)
    merged_df[['SNP']].to_csv('chr' + str(i) + '.snplist', header = None, index=False)


# In[ ]:





# In[ ]:




