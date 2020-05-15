import pandas as pd

filepath = 'scrubber/data_scrubbed.csv'
df = pd.read_csv(filepath)
pd.set_option('display.max_columns', None)
df['INCIDENT_TYPE'] = df['INCIDENT_1_OLD'].fillna('') + df['INCIDENT_TYPE_1'].fillna('')

df = df[[col for col in df if col not in ['INCIDENT_TYPE_1', 'INCIDENT_TYPE_2', 'INCIDENT_1_OLD', 'INCIDENT_TYPE_OTHER']] 
        + ['INCIDENT_TYPE_2', 'INCIDENT_TYPE_OTHER']]

df.to_csv('merged-data/merged_data.csv')

