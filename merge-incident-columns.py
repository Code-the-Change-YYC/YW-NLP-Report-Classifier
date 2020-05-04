#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


filepath = 'scrubber/data_scrubbed.csv'
df = pd.read_csv(filepath)
pd.set_option('display.max_columns', None)
df['INCIDENT_TYPE'] = df['INCIDENT_1_OLD'].fillna('') + df['INCIDENT_TYPE_1'].fillna('')


# In[3]:


df = df[[col for col in df if col not in ['INCIDENT_TYPE_1', 'INCIDENT_TYPE_2', 'INCIDENT_1_OLD', 'INCIDENT_TYPE_OTHER']] 
        + ['INCIDENT_TYPE_2', 'INCIDENT_TYPE_OTHER']]


# Incident Types will be at the end of the csv.

# In[4]:


df.to_csv('merged-data/merged_data.csv')

