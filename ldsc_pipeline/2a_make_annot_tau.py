#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import sys


# In[3]:


annot_d = 'ldscore/'
enrich_d = 'enrichment/'

annot_dfs = []
for i in np.arange(1, 23):
    df = pd.read_csv(annot_d + '1000G_EUR_geno.' + str(i) + '.annot.gz', compression='gzip', sep='\t')
    annot_dfs.append(df)
annot_f2 = pd.concat(annot_dfs, ignore_index=True)


# In[4]:


annot_full = annot_f2
annot_full = annot_full.drop(columns=['CHR', 'BP', 'CM'])
M_ref = len(annot_full)


# In[5]:


annot_sd = annot_full.iloc[:, 1:].apply(lambda x: x.std(skipna=True))


# In[6]:


annot_full = None
annot_dfs = None


# In[8]:


h2g = pd.read_csv(enrich_d + sys.argv[1] + '.delete', header=None)
ldsc_h2_part_delete_M = pd.read_csv(enrich_d + sys.argv[1] + '.part_delete', header=None, sep=' ')
n_jackknife = len(h2g)


# In[9]:


### calculate tau* and assoc p-value
output = ldsc_h2_part_delete_M.values * M_ref / h2g.values
sc_M = (annot_sd.values.reshape(-1, 1) * output.T).T
mean_sc = pd.DataFrame(sc_M).apply(lambda x: x.mean(skipna=True))
se_sc = pd.DataFrame(sc_M).apply(lambda x: (n_jackknife - 1) ** 2 /n_jackknife * x.var(skipna=True))
z_score = abs(mean_sc / se_sc)
taustar_p = (1 - stats.norm.cdf(z_score)) * 2

result = pd.read_csv(enrich_d + sys.argv[1] + '.results', sep='\t')

result['taustar'] = mean_sc
result['taustar_std_error'] = se_sc
result['taustar_p'] = taustar_p

result.to_csv(enrich_d + sys.argv[1] + '.h2.tsv', sep='\t', index=False)


# In[ ]:




