#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd


# In[67]:


filepath = 'scrubber/data_scrubbed.csv'
df = pd.read_csv(filepath)
pd.set_option('display.max_columns', None)
df['INCIDENT_TYPE'] = df['INCIDENT_1_OLD'].fillna('') + df['INCIDENT_TYPE_1'].fillna('')


# In[68]:


df.to_csv('merged-data/merged_data.csv')

